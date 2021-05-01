# import the pygame module, so you can use it
import datetime
import os

import pygame
import random
from glob import glob
from pygame.locals import *
from pathlib import PurePath

import sys
import os

from icecream import ic 
import pygame as pg
import pygame.freetype
import pygame.midi
from tinydb import TinyDB, Query

def print_device_info():
    pygame.midi.init()
    _print_device_info()
    pygame.midi.quit()


def _print_device_info():
    for i in range(pygame.midi.get_count()):
        r = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = r

        in_out = ""
        if input:
            in_out = "(input)"
        if output:
            in_out = "(output)"

        print(
            "%2i: interface :%s:, name :%s:, opened :%s:  %s"
            % (i, interf, name, opened, in_out)
        )


FPS = 60
FramePerSec = pygame.time.Clock()
pygame.freetype.init()

db = TinyDB("save.json")
fail = {} # {name : "D4", try:4, win : 5, fail : 3, last_date = datetime.now}
win = {}
# db.insert({"name" : "D4", "trial":4, "win" : 5, "fail" : 3, "last_date" : str(datetime.datetime.now())})

note_database = db.search(Query().name == "D4")
ic(note_database)

class Text():
	def __init__(self):
		super().__init__()
		self.GAME_FONT = pygame.freetype.Font(r"Q:\Box Sync\PYCHARM\Solfege\FONTS\texgyreschola-bold.otf", 24)
		self.text = "Some text"
		self.textsurface = self.GAME_FONT.render('Some Text', False, (0, 0, 0))

	def draw(self, surface):
		self.textsurface = self.GAME_FONT.render_to(surface, 'Some Text', False, (0, 0, 0))
		# surface.blit(self.textsurface, (0, 0))

	def drawTextCentered(self, surface, text, text_size, color):
		text_rect = self.GAME_FONT.get_rect(text, size=50)
		text_rect.center = surface.get_rect().center
		self.GAME_FONT.render_to(surface, text_rect, text, color, size=50)

class Help(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load(r"Q:\Box Sync\PYCHARM\Solfege\212468.image2.jpg")
		self.surf = pygame.Surface((self.image.get_size()))
		self.rect = self.surf.get_rect(center=(1000,1500))

	def draw(self, surface):
		surface.blit(self.image, self.rect)

class Note(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		glob_pattern = os.path.join(r"Q:\Box Sync\PYCHARM\Solfege\Images\49", '*')
		all_notes = sorted(glob(glob_pattern), key=os.path.getctime)

		new_note = all_notes[random.randint(0, len(all_notes) - 1)]
		self.new_note_name = PurePath(new_note).stem
		ic(self.new_note_name)
		self.image = pygame.image.load(new_note)
		self.surf = pygame.Surface((self.image.get_size()))
		self.rect = self.surf.get_rect(center=(1000, 1000))



	def random_note(self):

		glob_pattern = os.path.join(r"Q:\Box Sync\PYCHARM\Solfege\Images\49", '*4.png')
		all_notes = sorted(glob(glob_pattern), key=os.path.getctime)
		# ic(all_notes)

		new_note = all_notes[random.randint(0, len(all_notes)-1)]
		self.new_note_name = PurePath(new_note).stem

		self.image = pygame.image.load(new_note)


	def update(self, pressed_note):
		win = True

		ic(pressed_note)

		if self.new_note_name.find("b") != -1 or self.new_note_name.find("#") != -1 :
			note_list = ["A", "B", "C", 'D', "E", "F", "G"]

			if self.new_note_name.find("b") != -1:
				letter = self.new_note_name[0]
				equivalent_letter = note_list[note_list.index(letter)-1]
				new_note = str(str(self.new_note_name).replace(letter, equivalent_letter)).replace("b", "#")
				# ic("new note", new_note)
			if self.new_note_name.find("#") != -1:
				letter = self.new_note_name[0]
				try:
					equivalent_letter = note_list[note_list.index(letter)+1]
				except IndexError:
					equivalent_letter = note_list[0]
				new_note = str(str(self.new_note_name).replace(letter, equivalent_letter)).replace("#", "b")


			self.new_note_name_list = [self.new_note_name, new_note]
			print(f'Key pressed is {pressed_note}, looking for {" or ".join(self.new_note_name)}')
		else:
			print(f'Key pressed is {pressed_note}, looking for {self.new_note_name}')
			self.new_note_name_list = [str(self.new_note_name)]


		note_database = db.search(Query().name == self.new_note_name_list[0])

		if len(note_database) >0 and "trial" in note_database[0]:

			note_try = note_database[0]["trial"] +1
			note_fail = note_database[0]["fail"]
			note_win = note_database[0]["win"]
			note_date = str(note_database[0]["last_date"])
		else:
			note_name = self.new_note_name_list[0]
			db.insert({"name":note_name})
			note_try = 1
			note_fail = 0
			note_win = 0
			note_date = str(datetime.datetime.now())

		if pressed_note in self.new_note_name_list:
			note_win += 1

		else:
			win = False

			note_fail += 1
		self.random_note()

		db.update({"trial":note_try, "fail":note_fail, "win":note_win, "last_date":note_date}, Query().name == self.new_note_name_list[0])
		ic(db.search(Query().name == self.new_note_name_list[0]))

		return win



	def draw(self, surface):
		Instruction.drawTextCentered(surface, "test credt", 50, (0, 0, 0))
		surface.blit(self.image, self.rect)

	# define a main function

Guess = Note()
Helper = Help()
Instruction = Text()

def main(device_id=3):
	# initialize the pygame module
	pygame.init()
	# load and set the logo
	# logo = pygame.image.load(r"Q:\Box Sync\PYCHARM\Solfege\Images\A#0.png")
	# pygame.display.set_icon(logo)
	pygame.display.set_caption("minimal program")

	# create a surface on screen that has the size of 240 x 180
	screen = pygame.display.set_mode((2000, 2000))
	screen.fill(color=pygame.Color(255, 255, 255))


	pg.fastevent.init()
	event_get = pg.fastevent.get
	event_post = pg.fastevent.post

	pygame.midi.init()

	_print_device_info()

	if device_id is None:
		input_id = pygame.midi.get_default_input_id()
	else:
		input_id = device_id

	print("using input_id :%s:" % input_id)

	i = pygame.midi.Input(input_id)
	screen.fill((255, 255, 255))
	Instruction.drawTextCentered(screen, "Please play the right note", 50, (0, 0, 0))



	# define a variable to control the main loop
	running = True

	# main loop

	pressed_note = ""
	win = True
	played = False
	while running:
		pygame.display.flip()


		events = event_get()
		for e in events:
			if e.type in [pg.QUIT]:
				running = False
			if e.type in ["z"]:
				Guess.update("D4")

				# event handling, gets all event from the event queue
				pygame.display.update()
				FramePerSec.tick(FPS)
			if e.type in [pygame.midi.MIDIIN]:
				# ic(e)
				if e.data1 not in [2, 3] and e.status == 144:
					played = True
					pressed_note = pygame.midi.midi_to_ansi_note(e.data1)

					win = Guess.update(pressed_note)
					# ic(win)




					pygame.display.flip()
					pygame.display.update()


					# event handling, gets all event from the event queue

					FramePerSec.tick(FPS)
					print("\n\n-----------------------------------------------------------\n\n")

		if i.poll():
			midi_events = i.read(10)
			# convert them into pygame events.
			midi_evs = pygame.midi.midis2events(midi_events, i.device_id)

			for m_e in midi_evs:
				event_post(m_e)
		screen.fill((255, 255, 255))

		Guess.draw(screen)
		Helper.draw(screen)
		if not played:
			Instruction.drawTextCentered(screen, f"Please play the right note", 50, (0, 0, 0))
		if played:
			if win:
				Instruction.drawTextCentered(screen, f"You pressed {pressed_note}", 50, (0, 255, 0))
			else:
				Instruction.drawTextCentered(screen, f"You pressed {pressed_note}", 50, (255, 0, 0))



	del i
	pygame.midi.quit()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
	# call the main function
	main()