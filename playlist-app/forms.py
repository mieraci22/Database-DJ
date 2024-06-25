"""Forms for playlist app."""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class PlaylistForm(FlaskForm):
    """Form for adding playlists."""
    name = StringField('Playlist Name', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Create Playlist')

class SongForm(FlaskForm):
    """Form for adding songs."""
    title = StringField('Title', validators=[DataRequired()])
    artist = StringField('Artist', validators=[DataRequired()])
    submit = SubmitField('Add Song')

# DO NOT MODIFY THIS FORM - EVERYTHING YOU NEED IS HERE
class NewSongForPlaylistForm(FlaskForm):
    """Form for adding a song to playlist."""
    song = SelectField('Song To Add', coerce=int)