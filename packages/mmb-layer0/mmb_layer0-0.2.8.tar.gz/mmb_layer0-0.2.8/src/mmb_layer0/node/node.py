# 1 node has 1 blockchain and 1 WorldState
import ecdsa

from mmb_layer0.blockchain.chain.local_saver import ISaver, NotImplementedSaver
from mmb_layer0.blockchain.chain.saver_impl.filebase_saver import FilebaseSaver, FilebaseDatabase
from mmb_layer0.blockchain.core.chain import Chain
from mmb_layer0.blockchain.consensus.poa_consensus import ProofOfAuthority
from mmb_layer0.blockchain.core.transaction_type import Transaction, MintBurnTransaction
from mmb_layer0.blockchain.processor.block_processor import BlockProcessor
from mmb_layer0.blockchain.processor.transaction_processor import TransactionProcessor
from mmb_layer0.blockchain.core.validator import Validator
from mmb_layer0.blockchain.core.worldstate import WorldState
from mmb_layer0.config import MMBConfig
import typing
import os
from mmb_layer0.node.node_event_handler import NodeEventHandler
from mmb_layer0.utils.serializer import ChainSerializer

if typing.TYPE_CHECKING:
    from mmb_layer0.p2p.peer_type.remote_peer import RemotePeer
    from mmb_layer0.p2p.peer import Peer
from mmb_layer0.node.events.node_event import NodeEvent
from mmb_layer0.utils.crypto.signer import SignerFactory
from rich import print, inspect
from mmb_layer0.blockchain.core.block import Block

class Node:
    def __init__(self, dummy = False) -> None:
        print("node.py:__init__: Initializing Node")
        self.blockchain: Chain = Chain(dummy)

        self.worldState: WorldState = WorldState()

        self.worldState.get_eoa("0x0")

        self.nativeTokenSupply = int(MMBConfig.NativeTokenValue * MMBConfig.NativeTokenQuantity)

        self.chain_file = "chain.json"
        self.version = open("node_ver.txt", "r").read()

        self.signer = SignerFactory().instance.get_signer()

        self.publicKey, self.privateKey = self.signer.gen_key()
        self.address = self.signer.address(self.publicKey)

        # self.node_subscribtions = []
        # self.peers: list["Peer"] = []

        self.mintburn_nonce = 1

        print(f"{self.address[:4]}:node.py:__init__: Initialized node")

        self.node_event_handler = NodeEventHandler(self)

        #
        # TODO: Refactor this shit right here
        self.consensus = ProofOfAuthority(self.address, self.privateKey)
        self.blockchain.set_callbacks(self.consensus, self.execution, self.propose_block)

        self.origin = ""

        self.chain_file = f"{self.address}_chain.json"

        # self.saver = FilebaseSaver(FilebaseDatabase())
        self.saver = NotImplementedSaver()

        # TODO: Debugging purposes
        # self.load_chain_from_disk()

    def set_saver(self, saver: ISaver) -> None:
        self.saver = saver

    def load_chain_from_disk(self):
        chain = self.saver.load_chain()
        self.blockchain.reset_chain()
        self.saver.add_block(chain.chain[0]) # add genesis
        for block in chain.chain[1:]: # skip genesis again lol
            self.blockchain.add_block(block, initially=True)

    def save_chain_to_disk(self):
        self.saver.save_chain(self.blockchain)

    def propose_block(self, block: Block):
        self.node_event_handler.propose_block(block)

    def set_origin(self, origin: str) -> None:
        self.origin = origin


    def import_key(self, filename: str) -> None:
        self.publicKey, self.privateKey = self.signer.load(filename)
        self.address = self.signer.address(self.publicKey)
        self.consensus = ProofOfAuthority(self.address, self.privateKey)
        self.blockchain.set_callbacks(self.consensus, self.execution, self.node_event_handler.propose_block)
        print(f"{self.address[:4]}:node.py:import_key: Imported key " + self.address)

    def export_key(self, filename: str) -> None:
        self.signer.save(filename, self.publicKey, self.privateKey)
        print(f"{self.address[:4]}:node.py:export_key: Exported key " + self.address)


    # EVENT MANAGER
    # def subscribe(self, peer: "Peer"):
    #     # print(f"{self.origin}:node.py:subscribe: Subscribed to {peer.address}")
    #     # inspect(peer)
    #     self.node_event_handler.subscribe(peer)
    #
    # def broadcast(self, event: "NodeEvent"):
    #     self.node_event_handler.broadcast(event)
    #
    # def fire_to(self, peer: "RemotePeer", event: "NodeEvent"):
    #     self.node_event_handler.fire_to(peer, event)
    #
    # def process_event(self, event: "NodeEvent") -> bool:
    #     return self.node_event_handler.process_event(event)

    def mint(self, address: str, privateKey: any, publicKey: any) -> None:
        # print("node.py:faucet: Processing 100 native tokens to address")
        amount = int(100 * MMBConfig.NativeTokenValue)
        tx = MintBurnTransaction(address, amount, self.mintburn_nonce + 1, 0)
        self.mintburn_nonce += 1
        sign = self.signer.sign(tx.to_verifiable_string(), privateKey)
        self.propose_tx(tx, sign, publicKey)


    # def sync(self, other_json: str):
    #     # sync from another node
    #     other_obj = json.loads(other_json)
    #     print("node.py:sync: Syncing from " + other_obj["address"])
    #     blockchain_data = json.loads(other_obj["blockchain"])
    #     # Check height
    #     if self.blockchain.get_height() > blockchain_data["length"]:
    #         return

        # print(blockchain_data)
        # # Sync blocks
        # for i in range(self.blockchain.get_height(), blockchain_data["length"]):
        #     print(f"node.py:sync: Syncing block #{i}")
        #     block_data = blockchain_data["chain"][i]
        #     new_block = self.blockchain.add_block(BlockProcessor.cast_block(block_data))
        #     self.execution(new_block)

    # def check_sync(self, other_json: str):
    #     other_node = NodeSerializer.deserialize_node(other_json)
    #     return NodeSyncServices.check_sync(self, other_node)

    def get_height(self) -> int:
        return self.blockchain.get_height()

    def get_balance(self, address) -> int:
        return self.worldState.get_eoa(address).balance

    def get_native_token_supply(self) -> int:
        return self.nativeTokenSupply

    def get_nonce(self, address: str) -> int:
        return self.worldState.get_eoa(address).nonce

    def propose_tx(self, tx: Transaction, signature, publicKey: any):
        self.node_event_handler.broadcast(NodeEvent("tx", {
            "tx": tx,
            "signature": signature,
            "publicKey": SignerFactory().get_signer().serialize(publicKey)
        }, self.address))

        print(SignerFactory().get_signer().serialize(publicKey))

    def process_tx(self, tx: Transaction, signature, publicKey):
        print(f"{self.address[:4]}:node.py:process_tx: Add pool " + tx.Txtype + " transaction")

        # self.blockchain.temporary_add_to_mempool(tx)

        if not Validator.validate_transaction_with_worldstate(tx, self.worldState): # Validate transaction
            return

        print(f"{self.address[:4]}:node.py:process_tx: Give transaction to blockchain nonce: " + str(tx.nonce))
        # print(tx, signature, publicKey)


        self.blockchain.add_transaction(tx, signature, publicKey)

    def execution(self, block: Block):
        # Block execution only happend after block is processed
        excecutor = TransactionProcessor(block, self.worldState)
        excecutor.process()

        # Save block
        self.saver.add_block(block)

    # def save_chain(self):
    #     print("node.py:save_chain: Saving chain")
    #     chain_data = self.to_json()
    #     with open(self.chain_file, "w") as f:
    #         f.write(chain_data)
    #     print("node.py:save_chain: Saved chain")
    #
    # def load_chain(self):
    #     print("node.py:load_chain: Loading chain")
    #     chain_data = ""
    #     with open(self.chain_file, "r") as f:
    #         chain_data = f.read()
    #
    #     if chain_data == "":
    #         print("node.py:load_chain: No chain data found")
    #         return

        # self.blockchain = jsonlight.loads(Chain, chain_data)
        # self.blockchain.build_chain(chain_data)
        # self.blockchain.build_mempool(chain_data)
        # print("node.py:load_chain: Loaded chain")


    def debug(self):
        print(f"{self.address[:4]}:node.py:debug:-------------------------------Debug node----------------------")
        self.blockchain.debug_chain()
        print(self.worldState)
        print(self.address, self.publicKey, self.privateKey)
        print(f"{self.address[:4]}:node.py:debug:-------------------------------Debug node----------------------")