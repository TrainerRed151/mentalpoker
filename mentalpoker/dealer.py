from elgamal_suite import PublicKey, PrivateKey, PUBLIC_PARAMS
from random import shuffle

CARDS = ['Ac', '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', 'Tc', 'Jc', 'Qc', 'Kc', 'Ad', '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', 'Td', 'Jd', 'Qd', 'Kd', 'Ah', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', 'Th', 'Jh', 'Qh', 'Kh', 'As', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', 'Ts', 'Js', 'Qs', 'Ks']

# These globals assume default PUBLIC_PARAMS are used by players
# When custom params are used, new values are generated, but it adds time to initialization
RESIDUES = [2, 4, 5, 8, 9, 10, 11, 16, 17, 18, 20, 21, 22, 25, 29, 31, 32, 34, 36, 37, 39, 40, 41, 42, 44, 45, 49, 50, 53, 55, 57, 58, 61, 62, 64, 67, 68, 69, 71, 72, 73, 74, 78, 79, 80, 81, 82, 83, 84, 85, 88, 90]

class Dealer:
	def __init__(self, cards=CARDS, shuffle_key=None, crypto_params=PUBLIC_PARAMS):
		if PUBLIC_PARAMS == crypto_params and len(cards)<=52:
			residues = RESIDUES
		else:
			residues = generate_residues_from_params(crypto_params, len(cards))
		self.int_to_card={residues[i]:cards[i] for i in range(len(cards))}
		self.new_deck = residues
		self.crypto_params = crypto_params
		self.shuffle_key = shuffle_key
		if self.shuffle_key is None:
			self.shuffle_key = PrivateKey(public_params=self.crypto_params)
		self.decks = {}

	def shuffle(self, deck):
		encrypted = [self.shuffle_key.commutative_encrypt(card) for card in deck]
		shuffle(encrypted)
		return encrypted

	def deal(self, deck, shuffle_locked=True, deck_id="temp"):
		if shuffle_locked:
			deck = self.remove_shuffle_lock(deck)
		keys = [PrivateKey(public_params=self.crypto_params) for _ in range(len(deck))]
		self.decks[deck_id] = keys
		return [keys[i].commutative_encrypt(deck[i]) for i in range(len(deck))]

	def reveal_card(self, card, keys):
		value = [*card]
		for key in keys:
			value = key.commutative_decrypt(value)
		if type(value) is not int:
			raise ValueError("Provided keys not able to fully decrypt card")
		return self.int_to_card[value]

	def remove_shuffle_lock(self, deck):
		return [self.shuffle_key.commutative_decrypt(card) for card in deck]

	def get_card_key(self, index, deck_id="temp"):
		return self.get_deck_keys(deck_id)[index]

	def get_deck_keys(self, deck_id="temp"):
		return self.decks[deck_id]

def generate_residues_from_params(crypto_params, n):
	sk = PrivateKey(public_params=crypto_params)
	i = 2
	residues = []
	p = crypto_params[0]
	exp = (p - 1)//2
	while len(residues) < n:
		c = sk.encrypt(i)
		if pow(c[0], exp, p) == 1:
			residues.append(i)
		i += 1
	return residues

