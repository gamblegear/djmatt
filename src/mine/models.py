from django.db import models
from django.contrib.auth.models import User
# Create your models here.

COUNTRIES_CHOICES = (
    ("""Afghanistan""","""Afghanistan"""),("""Albania""","""Albania"""),("""Algeria""","""Algeria"""),("""Andorra""","""Andorra"""),("""Angola""","""Angola"""),("""Antigua and Barbuda""","""Antigua and Barbuda"""),("""Argentina""","""Argentina"""),("""Armenia""","""Armenia"""),("""Aruba""","""Aruba"""),("""Australia""","""Australia"""),("""Austria""","""Austria"""),("""Azerbaijan""","""Azerbaijan"""),("""Bahamas""","""Bahamas"""),("""Bahrain""","""Bahrain"""),("""Bangladesh""","""Bangladesh"""),("""Barbados""","""Barbados"""),("""Belarus""","""Belarus"""),("""Belgium""","""Belgium"""),("""Belize""","""Belize"""),("""Benin""","""Benin"""),("""Bhutan""","""Bhutan"""),("""Bolivia""","""Bolivia"""),("""Bosnia and Herzegovina""","""Bosnia and Herzegovina"""),("""Botswana""","""Botswana"""),("""Brazil""","""Brazil"""),("""Brunei ""","""Brunei """),("""Bulgaria""","""Bulgaria"""),("""Burkina Faso""","""Burkina Faso"""),("""Burma""","""Burma"""),("""Burundi""","""Burundi"""),("""Cambodia""","""Cambodia"""),("""Cameroon""","""Cameroon"""),("""Canada""","""Canada"""),("""Cape Verde""","""Cape Verde"""),("""Central African Republic""","""Central African Republic"""),("""Chad""","""Chad"""),("""Chile""","""Chile"""),("""China""","""China"""),("""Colombia""","""Colombia"""),("""Comoros""","""Comoros"""),("""Congo, Democratic Republic of the""","""Congo, Democratic Republic of the"""),("""Congo, Republic of the""","""Congo, Republic of the"""),("""Costa Rica""","""Costa Rica"""),("""Cote d'Ivoire""","""Cote d'Ivoire"""),("""Croatia""","""Croatia"""),("""Cuba""","""Cuba"""),("""Curacao""","""Curacao"""),("""Cyprus""","""Cyprus"""),("""Czech Republic""","""Czech Republic"""),("""Denmark""","""Denmark"""),("""Djibouti""","""Djibouti"""),("""Dominica""","""Dominica"""),("""Dominican Republic""","""Dominican Republic"""),("""East Timor (see Timor-Leste)""","""East Timor (see Timor-Leste)"""),("""Ecuador""","""Ecuador"""),("""Egypt""","""Egypt"""),("""El Salvador""","""El Salvador"""),("""Equatorial Guinea""","""Equatorial Guinea"""),("""Eritrea""","""Eritrea"""),("""Estonia""","""Estonia"""),("""Ethiopia""","""Ethiopia"""),("""Fiji""","""Fiji"""),("""Finland""","""Finland"""),("""France""","""France"""),("""Gabon""","""Gabon"""),("""Gambia, The""","""Gambia, The"""),("""Georgia""","""Georgia"""),("""Germany""","""Germany"""),("""Ghana""","""Ghana"""),("""Greece""","""Greece"""),("""Grenada""","""Grenada"""),("""Guatemala""","""Guatemala"""),("""Guinea""","""Guinea"""),("""Guinea-Bissau""","""Guinea-Bissau"""),("""Guyana""","""Guyana"""),("""Haiti""","""Haiti"""),("""Holy See""","""Holy See"""),("""Honduras""","""Honduras"""),("""Hong Kong""","""Hong Kong"""),("""Hungary""","""Hungary"""),("""Iceland""","""Iceland"""),("""India""","""India"""),("""Indonesia""","""Indonesia"""),("""Iran""","""Iran"""),("""Iraq""","""Iraq"""),("""Ireland""","""Ireland"""),("""Israel""","""Israel"""),("""Italy""","""Italy"""),("""Jamaica""","""Jamaica"""),("""Japan""","""Japan"""),("""Jordan""","""Jordan"""),("""Kazakhstan""","""Kazakhstan"""),("""Kenya""","""Kenya"""),("""Kiribati""","""Kiribati"""),("""Korea, North""","""Korea, North"""),("""Korea, South""","""Korea, South"""),("""Kosovo""","""Kosovo"""),("""Kuwait""","""Kuwait"""),("""Kyrgyzstan""","""Kyrgyzstan"""),("""Laos""","""Laos"""),("""Latvia""","""Latvia"""),("""Lebanon""","""Lebanon"""),("""Lesotho""","""Lesotho"""),("""Liberia""","""Liberia"""),("""Libya""","""Libya"""),("""Liechtenstein""","""Liechtenstein"""),("""Lithuania""","""Lithuania"""),("""Luxembourg""","""Luxembourg"""),("""Macau""","""Macau"""),("""Macedonia""","""Macedonia"""),("""Madagascar""","""Madagascar"""),("""Malawi""","""Malawi"""),("""Malaysia""","""Malaysia"""),("""Maldives""","""Maldives"""),("""Mali""","""Mali"""),("""Malta""","""Malta"""),("""Marshall Islands""","""Marshall Islands"""),("""Mauritania""","""Mauritania"""),("""Mauritius""","""Mauritius"""),("""Mexico""","""Mexico"""),("""Micronesia""","""Micronesia"""),("""Moldova""","""Moldova"""),("""Monaco""","""Monaco"""),("""Mongolia""","""Mongolia"""),("""Montenegro""","""Montenegro"""),("""Morocco""","""Morocco"""),("""Mozambique""","""Mozambique"""),("""Namibia""","""Namibia"""),("""Nauru""","""Nauru"""),("""Nepal""","""Nepal"""),("""Netherlands""","""Netherlands"""),("""Netherlands Antilles""","""Netherlands Antilles"""),("""New Zealand""","""New Zealand"""),("""Nicaragua""","""Nicaragua"""),("""Niger""","""Niger"""),("""Nigeria""","""Nigeria"""),("""North Korea""","""North Korea"""),("""Norway""","""Norway"""),("""Oman""","""Oman"""),("""Pakistan""","""Pakistan"""),("""Palau""","""Palau"""),("""Palestinian Territories""","""Palestinian Territories"""),("""Panama""","""Panama"""),("""Papua New Guinea""","""Papua New Guinea"""),("""Paraguay""","""Paraguay"""),("""Peru""","""Peru"""),("""Philippines""","""Philippines"""),("""Poland""","""Poland"""),("""Portugal""","""Portugal"""),("""Qatar""","""Qatar"""),("""Romania""","""Romania"""),("""Russia""","""Russia"""),("""Rwanda""","""Rwanda"""),("""Saint Kitts and Nevis""","""Saint Kitts and Nevis"""),("""Saint Lucia""","""Saint Lucia"""),("""Saint Vincent and the Grenadines""","""Saint Vincent and the Grenadines"""),("""Samoa ""","""Samoa """),("""San Marino""","""San Marino"""),("""Sao Tome and Principe""","""Sao Tome and Principe"""),("""Saudi Arabia""","""Saudi Arabia"""),("""Senegal""","""Senegal"""),("""Serbia""","""Serbia"""),("""Seychelles""","""Seychelles"""),("""Sierra Leone""","""Sierra Leone"""),("""Singapore""","""Singapore"""),("""Sint Maarten""","""Sint Maarten"""),("""Slovakia""","""Slovakia"""),("""Slovenia""","""Slovenia"""),("""Solomon Islands""","""Solomon Islands"""),("""Somalia""","""Somalia"""),("""South Africa""","""South Africa"""),("""South Korea""","""South Korea"""),("""South Sudan""","""South Sudan"""),("""Spain ""","""Spain """),("""Sri Lanka""","""Sri Lanka"""),("""Sudan""","""Sudan"""),("""Suriname""","""Suriname"""),("""Swaziland ""","""Swaziland """),("""Sweden""","""Sweden"""),("""Switzerland""","""Switzerland"""),("""Syria""","""Syria"""),("""Taiwan""","""Taiwan"""),("""Tajikistan""","""Tajikistan"""),("""Tanzania""","""Tanzania"""),("""Thailand ""","""Thailand """),("""Timor-Leste""","""Timor-Leste"""),("""Togo""","""Togo"""),("""Tonga""","""Tonga"""),("""Trinidad and Tobago""","""Trinidad and Tobago"""),("""Tunisia""","""Tunisia"""),("""Turkey""","""Turkey"""),("""Turkmenistan""","""Turkmenistan"""),("""Tuvalu""","""Tuvalu"""),("""Uganda""","""Uganda"""),("""Ukraine""","""Ukraine"""),("""United Arab Emirates""","""United Arab Emirates"""),("""United Kingdom""","""United Kingdom"""),("""Uruguay""","""Uruguay"""),("""Uzbekistan""","""Uzbekistan"""),("""Vanuatu""","""Vanuatu"""),("""Venezuela""","""Venezuela"""),("""Vietnam""","""Vietnam"""),("""Yemen""","""Yemen"""),("""Zambia""","""Zambia"""),("""Zimbabwe""","""Zimbabwe"""),)
GENDER_CHOICES =(
    ("Male","Male"),("Female","Female"),("No_Response","No Response")
    )
AGREE_CHOICES = (
    (1,1),
    (2,2),
    (3,3),
    (4,4),
    (5,5),
    (6,6),
    (7,7),
    )


class UserProfile(models.Model):
    id = models.AutoField(primary_key = True)
    user = models.OneToOneField(User)
    name = models.CharField(max_length = 200)   #as uid
    is_admin = models.BooleanField(default=False)
    final_time = models.DateTimeField(blank=True, null=True)
    final_time_two = models.DateTimeField(blank=True, null=True)
    random_code = models.CharField(max_length = 10)
    def __unicode__(self):
        return self.user.username

class UserSurvey(models.Model):
    id = models.AutoField(primary_key = True)
    nationality = models.CharField(max_length = 50, choices = COUNTRIES_CHOICES)
    gender = models.CharField(max_length = 11, choices = GENDER_CHOICES)
    agree = models.IntegerField(verbose_name ='Generally speaking, most people can be trusted.(1 is strongly disagree, 7 is strongly agree)', choices = AGREE_CHOICES)
    user_profile = models.OneToOneField(UserProfile)
    def __unicode__(self):
        return self.user_profile.user.username
    

class Game(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 200)
    rows = models.IntegerField(default=0)
    columns = models.IntegerField(default=0)
    groups_num = models.IntegerField(default=0)
    panels_per_group = models.IntegerField(default=0)
    wait_time = models.IntegerField(default=0)
    create_time = models.DateTimeField(blank=True, null=True)
    is_activated = models.BooleanField(default=False)
    total_time = models.IntegerField(blank=True, null=True, default=0)
    warning_time = models.IntegerField(blank=True, null=True, default=0)
    switch_cost = models.IntegerField(blank=True, null=True, default=0)
    
class Group(models.Model):
    id = models.AutoField(primary_key = True)
    game = models.ForeignKey(Game)
    name = models.CharField(blank=True, null=True, max_length = 200)
    score_1 = models.IntegerField(default = 0)
    score_2 = models.IntegerField(default = 0)

class Panel(models.Model):
    id = models.AutoField(primary_key = True)
    session = models.IntegerField(default = 0)
    user = models.ForeignKey(User)
    game = models.ForeignKey(Game)
    group = models.ForeignKey(Group)
    progress = models.TextField(blank=True, null=True)
    name = models.CharField(blank=True, null=True, max_length = 200)

class Log(models.Model):
    id = models.AutoField(primary_key = True)
    game = models.ForeignKey(Game)
    group = models.ForeignKey(Group)
    panel = models.ForeignKey(Panel)
    user_profile = models.ForeignKey(UserProfile)
    action = models.CharField(max_length = 200)
    action_time = models.DateTimeField(blank=True, null=True)


