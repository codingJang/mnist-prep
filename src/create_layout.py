from cryptography.hazmat.primitives.serialization import load_pem_private_key
from securesystemslib.signer import CryptoSigner
from in_toto.models.layout import Layout, Step, Inspection
from in_toto.models.metadata import Envelope, Metablock
# https://github.com/in-toto/in-toto/issues/663
from in_toto.models._signer import load_public_key_from_file

def main():
  # Load Alice's private key to later sign the layout
  with open("alice", "rb") as f:
    key_alice = load_pem_private_key(f.read(), None)

  signer_alice = CryptoSigner(key_alice)
  
  # Fetch and load Bob's, Carl's, Diana's, and Elenor's public keys
  key_bob = load_public_key_from_file("../Bob/bob.pub")
  key_carl = load_public_key_from_file("../Carl/carl.pub")
  key_diana = load_public_key_from_file("../Diana/diana.pub")
  key_elenor = load_public_key_from_file("../Elenor/elenor.pub")
  print(key_bob)

  layout = Layout()
  for key in [key_bob, key_carl, key_diana, key_elenor]:
    layout.add_functionary_key(key) ### ?
  layout.set_relative_expiration(months=4)

  step_clone = Step(name="clone")
  step_clone.pubkeys = [key_bob.keyid]
  step_clone.set_expected_command_from_string(
    "git clone https://github.com/codingJang/mnist-project.git")
  step_clone.add_product_rule_from_string("CREATE mnist-project/src/net.py")
  step_clone.add_product_rule_from_string("CREATE mnist-project/src/train.py")
  step_clone.add_product_rule_from_string("DISALLOW *")
  
  metadata = Envelope.from_signable(layout)

  # Sign and dump layout to "root.layout"
  metadata.create_signature(signer_alice)
  metadata.dump("root.layout")
  print('Created demo in-toto layout as "root.layout".')

if __name__ == '__main__':
  main()
