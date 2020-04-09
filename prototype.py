"""
First prototype of the project.
We have one or two blocs :
	- that are square (no matter their shape in this prototype)
	- whose the mass, the initial velocity and position are given (no acceleration)
	- moving along the same and unique horizontal axis
	- there is no loss of energy when blocks collide together or with a wall
	- there can be friction with the ground only (not air)

We can :
	- activate / desactivate the side walls
	- make the two blocs collide each other, and know what their velocity and position will be
	- obviously count the number of collisions between the blocks, if only the left side wall is enabled
"""


class Block:
	"""
	This class allows us to simply create and manage blocks.
	"""
	def __init__(self):
		print("Block created !")


def main():
	pass


if __name__ == "__main__":
	main()