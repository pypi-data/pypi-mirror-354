This Python's biblioteque can "play" the notes and she can download YOUR music.

She's got two modules: note and load_music

Note module's call is:

    import pythons_musicals

    <yourNoteVariable> = pythons_musicals.note.load(<note>)

    if __name__ == "__main__":
        <yourNoteVariable>.play()

and load_music module's call is:

    import pythons_musicals

    <SoundVariable> = pythons_muscals.load_music.load(<yourDirectory>)

    if __name__ == "__main__":
        <SoundVariable>.start()

ATTENTION!

note module's got method play(), and load_music module's got method start()

And don't forget write 
    from pythons_musicals.sounds import *
