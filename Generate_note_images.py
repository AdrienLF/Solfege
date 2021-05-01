import abjad
from PIL import Image
import multiprocessing

print(abjad.__version__)

note_letters = ["C", "D", "E", "F", "G", "A", "B"]
note_numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]


piano = abjad.Piano()
print(piano.pitch_range)

piano_note_lists = [x + y for x in note_letters for y in note_numbers]


sorted_note_list = sorted(piano_note_lists, key= lambda x: x[1])
print(sorted_note_list[14:43])

note_dict = dict(enumerate(sorted_note_list[14:43]))

bass_notes = sorted_note_list[14:43][:15]
treble_notes = sorted_note_list[14:43][14:]

print(bass_notes)
print(treble_notes)

# treble_notes =


duration = abjad.Duration(1, 4)

notes = [abjad.Note(pitch, duration) for pitch in bass_notes]
staff = abjad.Staff(notes)
clef = abjad.Clef('bass')
abjad.attach(clef, staff[0])
abjad.attach(piano, staff[0])
# abjad.show(piano.pitch_range)
# abjad.show(staff)

string = "d'8 f' a' d'' f'' gs'4 r8 e' gs' b' e'' gs'' a'4"
voice = abjad.Voice(string, name="RH_Voice")
staff = abjad.Staff([voice], name="RH_Staff")
score = abjad.Score([staff], name="Score")

sharps = ["C#", "D#", "F#", "G#", "A#"]
flat = ["Db", "Eb", "Gb", "Ab", "Bb"]

sharp_note_lists = [x + y for x in sharps for y in note_numbers]
flat_note_lists = [x + y for x in flat for y in note_numbers]
# print(sharp_note_lists)
# print(flat_note_lists)

easy_mode = False
def define_clef(note):

	note_object = abjad.NamedPitch(note)
	bass_range = abjad.PitchRange("[A0, C4]")

	if note_object.number in bass_range:
		return "bass"
	else:
		return "treble"


def render_image(note):
	duration = abjad.Duration(1, 4)

	score = abjad.Note(note, duration)

	staff = abjad.Staff([score])
	clef = abjad.Clef(define_clef(note))
	time_signature = abjad.TimeSignature((4, 4), hide=True)
	abjad.attach(time_signature, staff[0], context="Score", tag=abjad.Tag("+PARTS"))
	abjad.attach(clef, staff[0])
	if easy_mode:
		abjad.label(score).with_pitches(locale="us")
	# abjad.show(score)
	abjad.persist.as_png(score, png_file_path=rf"Q:\Box Sync\PYCHARM\Solfege\{note}", remove_ly=True, resolution=1200)

	im = Image.open(rf"Q:\Box Sync\PYCHARM\Solfege\{note}.png")
	left = 1070
	top = 207
	right = 2550
	bottom = 2380

	# Cropped image of above dimension
	# (It will not change orginal image)
	im1 = im.crop((left, top, right, bottom))
	im1.save(rf"Q:\Box Sync\PYCHARM\Solfege\{note}.png")

for note in flat_note_lists:
	define_clef(note)

if __name__ ==  '__main__':
	print(multiprocessing.cpu_count())
	pool = multiprocessing.Pool(multiprocessing.cpu_count()-1)
	for note in bass_notes:
		p = pool.apply_async(render_image, args=(note,))



	for note in treble_notes:
		p = pool.apply_async(render_image, args=(note,))

	for note in sharp_note_lists:
		p = pool.apply_async(render_image, args=(note,))

	for note in flat_note_lists:
		p = pool.apply_async(render_image, args=(note,))

	pool.close()
	pool.join()