from flask import Flask, redirect, render_template, request, flash
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Playlist, Song, PlaylistSong
from forms import NewSongForPlaylistForm, SongForm, PlaylistForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playlist-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

connect_db(app)



if __name__ == '__main__':
    app.run(debug=True)



@app.route("/")
def root():
    """Homepage: redirect to /playlists."""
    return redirect("/playlists")

##############################################################################
# Playlist routes

@app.route("/playlists")
def show_all_playlists():
    """Return a list of playlists."""
    playlists = Playlist.query.all()
    return render_template("playlists.html", playlists=playlists)

@app.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
    """Show detail on specific playlist."""
    playlist = Playlist.query.get_or_404(playlist_id)
    return render_template("playlist.html", playlist=playlist)

@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    """Handle add-playlist form."""
    form = PlaylistForm()
    if form.validate_on_submit():
        new_playlist = Playlist(name=form.name.data, description=form.description.data)
        db.session.add(new_playlist)
        db.session.commit()
        flash('Playlist created!', 'success')
        return redirect("/playlists")
    return render_template("add_playlist.html", form=form)

##############################################################################
# Song routes

@app.route("/songs")
def show_all_songs():
    """Show list of songs."""
    songs = Song.query.all()
    return render_template("songs.html", songs=songs)

@app.route("/songs/<int:song_id>")
def show_song(song_id):
    """Return a specific song."""
    song = Song.query.get_or_404(song_id)
    return render_template("song.html", song=song)

@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    """Handle add-song form."""
    form = SongForm()
    if form.validate_on_submit():
        new_song = Song(title=form.title.data, artist=form.artist.data)
        db.session.add(new_song)
        db.session.commit()
        flash('Song added!', 'success')
        return redirect("/songs")
    return render_template("add_song.html", form=form)


@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Add a song to playlist and redirect to list."""
    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm()

    # Restrict form to songs not already on this playlist
    curr_on_playlist = [s.id for s in playlist.songs]
    form.song.choices = (db.session.query(Song.id, Song.title)
                        .filter(Song.id.notin_(curr_on_playlist))
                        .all())

    # Convert the result to a list of tuples
    form.song.choices = [(str(id), title) for id, title in form.song.choices]

    if form.validate_on_submit():
        playlist_song = PlaylistSong(song_id=form.song.data, playlist_id=playlist_id)
        db.session.add(playlist_song)
        db.session.commit()
        flash('Song added to playlist!', 'success')
        return redirect(f"/playlists/{playlist_id}")

    return render_template("add_song_to_playlist.html", playlist=playlist, form=form)

if __name__ == '__main__':
    app.run(debug=True)