from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL , NumberRange, Length
from wtforms import ValidationError
import re


class ShowForm(Form):
    artist_id = StringField(
        'artist_id',
        validators=[DataRequired()]
    )
    venue_id = StringField(
        'venue_id',
        validators=[DataRequired()]
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone', validators=[DataRequired()]
    )

    genres = SelectMultipleField(
        """
        theses number is corresponding to the ID
        of theses genres in the genre table.
        """
        # TODO implement enum restriction --- not REQUIRED !!!!!!!!!!!!*********
        'genres', validators=[DataRequired()],
        choices = [
            ('1', 'Alternative'),
            ('2', 'Blues'),
            ('3', 'Classical'),
            ('4', 'Country'),
            ('5', 'Electronic'),
            ('6', 'Folk'),
            ('7', 'Funk'),
            ('8', 'Hip-Hop'),
            ('9', 'Heavy Metal'),
            ('10', 'Instrumental'),
            ('11', 'Jazz'),
            ('12', 'Musical Theatre'),
            ('13', 'Pop'),
            ('14', 'Punk'),
            ('15', 'R&B'),
            ('16', 'Reggae'),
            ('17', 'Rock n Roll'),
            ('18', 'Soul'),
            ('19', 'Other'),
        ]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website_link = StringField(
        # TODO implement enum restriction
        'website_link', validators=[URL()]
    )
    image_link= StringField(
        # TODO implement enum restriction
        'image_link', validators=[URL()]
    )

    """
        no validation needed
        as leaving both of them is information by it self.
    """
    seeking = BooleanField(
        'seeking'
    )
    seeking_description = StringField(
        'seeking_description'
    )

    def validate_phone(self, field):
        format = "^[0][1][0-9]*";
        length = 11
        message = "please enter a valid egypiton mobile number";
        data = field.data;
        match = re.search(format, data);

        print("info", length, match);
        if len(data) != length:
            raise ValidationError(message);
        if not match:
            raise ValidationError(message);
        print("valid phone number");

class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    phone = StringField(
        'phone',
        validators=[DataRequired()]
    )
    image_link = StringField(
        # repeated
        'image_link'
    )
    genres = SelectMultipleField(
        """
        theses number is corresponding to the ID
        of theses genres in the genre table.
        """
        # TODO implement enum restriction --- not REQUIRED !!!!!!!!!!!!*********
        'genres', validators=[DataRequired()],
        choices=[
            ('1', 'Alternative'),
            ('2', 'Blues'),
            ('3', 'Classical'),
            ('4', 'Country'),
            ('5', 'Electronic'),
            ('6', 'Folk'),
            ('7', 'Funk'),
            ('8', 'Hip-Hop'),
            ('9', 'Heavy Metal'),
            ('10', 'Instrumental'),
            ('11', 'Jazz'),
            ('12', 'Musical Theatre'),
            ('13', 'Pop'),
            ('14', 'Punk'),
            ('15', 'R&B'),
            ('16', 'Reggae'),
            ('17', 'Rock n Roll'),
            ('18', 'Soul'),
            ('19', 'Other'),
        ]
    )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[URL()]
    )
    website_link = StringField(
        # TODO implement enum restriction
        'website_link', validators=[URL()]
    )
    image_link= StringField(
        # TODO implement enum restriction
        'image_link', validators=[URL()]
    )

    """
        no validation needed
        as leaving both of them is information by it self.
    """
    seeking = BooleanField(
        'seeking'
    )
    seeking_description = StringField(
        'seeking_description'
    )

    def validate_phone(self, field):
        format = "^[0][1][0-9]*";
        length = 11
        data = field.data;
        message = "please enter a valid egypiton mobile number";

        match = re.search(format, data);
        print("info", length, match);
        if len(data) != length:
            raise ValidationError(message);
        if not match:
            raise ValidationError(message);


