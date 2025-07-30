#About#
##What's this##
This biblioteque download YOUR music, but she can "play" her notes
##Using##
She's got 2 modules: note and load_music

note module's call is:

    import pythons-musicals

    <your_note_variable> = pythons-musicals.note.load(<your_sound>)

    if __name__ == "__main__":
        <your_note_variable>.play()

and load_music module's call is:

    ...<your_sound> = pythons-musicals.load_music.load(<your_directory>)
    if __name__ == "__main__":
        <your_sound>.start()