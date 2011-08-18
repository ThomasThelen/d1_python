#!/usr/bin/env python

# Stdlib.
import datetime
import random

# D1.
import d1_common.types.generated.dataoneTypes

object_formats = [
  'eml://ecoinformatics.org/eml-2.0.0',
  'eml://ecoinformatics.org/eml-2.0.1',
  'eml://ecoinformatics.org/eml-2.1.0',
  'FGDC-STD-001.1-1999',
  'eml://ecoinformatics.org/eml-2.1.1',
  'FGDC-STD-001-1998',
  'INCITS 453-2009',
  'http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2',
  'CF-1.0',
  'CF-1.1',
  'CF-1.2',
  'CF-1.3',
  'CF-1.4',
  'http://www.cuahsi.org/waterML/1.0/',
  'http://www.cuahsi.org/waterML/1.1/',
  'http://www.loc.gov/METS/',
  'netCDF-3',
  'netCDF-4',
  'text/plain',
  'text/csv',
  'image/bmp',
  'image/gif',
  'image/jp2',
  'image/jpeg',
  'image/png',
  'image/svg+xml',
  'image/tiff',
  'http://rs.tdwg.org/dwc/xsd/simpledarwincore/',
  'http://digir.net/schema/conceptual/darwin/2003/1.0/darwin2.xsd',
  'application/octet-stream',
]

subjects = [
  'santa=purposefully=3775',
  '4782@rigorously@seekers',
  '5227@manuscript@objectively',
  '6011~recoiled~apologist',
  'stalled/squawk/5912',
  'blocking_687',
  '3934~senators',
  '8335_flick_cogitate',
  'sparingly~renault~9208',
  '8920_skye_fondled',
  'folding_5087',
  '9810_paranormal',
  'authenticators-733',
  'artfully/3822',
  'singing.3369',
  '7408@outskirts@absorbency',
  'profiteers=7446',
  'melanie~1855',
  '975@shadily',
  'slugs@6367',
  '5790=customizations',
  'dressed_sublist_1687',
  'equilibrate_8593',
  'stoles=propane=9017',
  '357~western',
  '7491~mystery',
  '1316.ploys',
  'reentered~2695',
  '9376.freon.purporter',
  '7009~observance~roving',
  '4664~tapestries',
  'render.stewardess.5267',
  '789@netherlands@paraboloid',
  'conferred=lurches=5154',
  'selectric~2975',
  '6705.touch.avignon',
  '4320@missionaries@mutability',
  'wronged-7700',
  '9615@breach@magill',
  'deplorable=5891',
  '6592~unicorns',
  '2775~leona~preempt',
  '7309/optical',
  '3724~responsive~ministries',
  '275_martians_aquarius',
  '3974.treetops',
  'exchanging-reinforcements-7818',
  'awarder~7223',
  'tiber~justifying~1796',
  '8067_diffuse',
  '1871-indomitable-straggle',
  '6212.malay.platforms',
  'reworked~8676',
  '433-fission-malta',
  'vegetated/1650',
  '851@combines',
  '7484@zeroed@rehearsal',
  'clenches-2049',
  '8145@punished@alleviation',
  'eros=6864',
  '8841-moment-disarms',
  '1594-flatness',
  '9397~paroling',
  'gaped/9228',
  '1825_redouble',
  '8255~detective',
  'matrimonial~beachhead~3578',
  'instructor.radially.2226',
  '9395@scares@shulman',
  '5819~operate',
  '5161-hebe',
  'descends=knolls=8054',
  'unfamiliarly@citizen@4703',
  '5495-disgusts-ledger',
  'zaire.5691',
  'solvents=zeroing=8956',
  'whitewater/sours/4623',
  'bivouac-seers-2425',
  '9491=comparably',
  'all~babe~9779',
  'pedagogic.salesian.1738',
  'cellular_stouffer_4330',
  '6191.perfectionist',
  '7365.esoteric',
  '1845-inbreed-depths',
  'lays-9905',
  '8416-oxidized',
  'enmity-5176',
  'plurality.design.4874',
  '6390/subspace',
  'observant=reconstruction=6040',
  'vanishingly~fixing~3170',
  'cohesively@1058',
  '607/chided/chesterfield',
  '5685@abolishers',
  'propagated=hoard=3091',
  '846=dostoevsky',
  'evensen.9937',
  'mailmen-6496',
  '2215_sunned',
]

rights_holders = [
  'INEPT~1195',
  'THETIS.MARTY.4523',
  '222=WHITEST=PITCH',
  '3182-DUPLICATORS',
  'NOLAN@4722',
  '9875@GRATIFICATION',
  'BRAZENNESS.QUACK.2675',
  '5295=SCARF=ANNUM',
  'FALL=5401',
  '1130-RHYTHM',
  '231/PROUST',
  'SINGINGLY@2938',
  'SENSELESSNESS.5523',
  'MARCIA@4853',
  '537~BAYOU~DECIBEL',
  '1380-EMITTED-NOUNS',
  '1826-ITALICS',
  'FURROWED.ADJUSTING.2950',
  '2124@METHODICALLY@DEFAULTS',
  'ALTERCATION.DABBLES.1988',
  '1854=SECTARIAN',
  'LYNDON.7590',
  '9761/DE',
  '8157~CONTINUOUSLY~HUNCHED',
  'DEFORESTATION.1704',
  'ARGUMENTATION@5529',
  'DISJUNCTION-5299',
  '9781=TEACH=IMPLANTS',
  'TRANSIENT~3325',
  '6041~ENLIGHTEN~REASON',
  '2252=KOBAYASHI=NONORTHOGONALITY',
  '655_COMBAT_AEGIS',
  'CLUMPED-FONT-3186',
  'APATHY_5885',
  'BIOMEDICAL/9200',
  '3854@BUDGETERS@PARADOXICALLY',
  '9348_FLIGHT',
  '5041=GROSSEST=APRICOT',
  '8988@BUBBLE',
  '5975/SHIFT',
  '672=CRUDER',
  'COED-BROTHERLINESS-8587',
  'FROZENLY-BEGGAR-8017',
  '1063=SOMATIC=EXEMPLIFY',
  '8875@UNNERVED',
  'DELICIOUSLY~AMPLY~1911',
  '3017-DEGRADE',
  'FOOLING~1418',
  'CINERAMA=BISCUIT=7490',
  'BREAKTHROUGH.PINE.5780',
  'ATOMICALLY.FRIENDLIER.9406',
  'SLAUGHTERING=5272',
  '4946@RISKY',
  '9184~EYEBROWS',
  'MUSCAT@MEASUREMENTS@9820',
  '2842_DEMORALIZED_SISYPHEAN',
  '1003@PERSIANIZATIONS@CORNFIELDS',
  '1564@OVERESTIMATION',
  '5675-GENTEEL',
  'BLANKETED/DISCOVER/5139',
  'GINGERLY_MADRID_1538',
  'FUNEREAL_2812',
  'CHOOSING.8443',
  'PROHIBITIVE-COOPED-8952',
  'MYSTERIES=FLUENTLY=9387',
  'HARLOTS@JUTLAND@9387',
  'ITINERARY@4453',
  '2211-MORRISON-UNIFORMLY',
  '4791@MAVERICK@DETERMINATE',
  '6272@GRACEFUL',
  '188=BRIBED=HOBBES',
  '400-GAPS-ADMINISTRATIVELY',
  '1780~SALZ',
  'TASTER.LAUNCHING.1611',
  '4478-DECADENCE-VERDI',
  '9939_HOTTER_BUXTEHUDE',
  '1131~SPEEDOMETER',
  'SPECIALIZE~EMULATOR~6740',
  '8762_FLAVOR',
  'CENSURES_PREDETERMINATION_6576',
  'BANISHMENT=CUMULATIVELY=9571',
  '5527-HAULS',
  '1568-IMAGINABLE',
  'IDEMPOTENT@9452',
  'SNEAKER~9598',
  'TELEVISIONS/LACERATED/5521',
  '1779-SEER-MERINGUE',
  '8846/REFERRAL/ALLEYS',
  'CIRCUMPOLAR=8016',
  '695-IMPRINTING-TAILORING',
  'CERTIFICATIONS=WHITTAKER=1851',
  '5462_DUBHE_CAUTIONER',
  '9369~GERHARD',
  '9243-STUDIOUSLY',
  '7004@FALKLANDS',
  '4585-LEARNS-BONHAM',
  'WATCHWORD@9799',
  'BRIEFED~DECOMPOSITIONS~1703',
  '9957-GLIDES-INDIGNANTLY',
  '4101/AWAIT',
]


def generate_random_sysmeta(pid, size, md5):
  sysmeta = d1_common.types.generated.dataoneTypes.systemMetadata()
  sysmeta.identifier = pid

  format_id = random.choice(object_formats)
  object_format = d1_common.types.generated.dataoneTypes.ObjectFormat(format_id)
  object_format.fmtid = format_id
  object_format.formatName = format_id
  object_format.scienceMetadata = False
  sysmeta.objectFormat = object_format

  sysmeta.size = size
  sysmeta.submitter = random.choice(subjects)
  sysmeta.rightsHolder = random.choice(rights_holders)
  sysmeta.checksum = d1_common.types.generated.dataoneTypes.checksum(md5)
  sysmeta.checksum.algorithm = 'MD5'
  sysmeta.dateUploaded = datetime.datetime.now()
  sysmeta.dateSysMetadataModified = datetime.datetime.now()
  sysmeta.originMemberNode = 'MN1'
  sysmeta.authoritativeMemberNode = 'MN1'

  # Debugging.
  #import pyxb
  #pyxb.RequireValidWhenGenerating(False)
  #print sysmeta.toxml()

  return sysmeta


def generate_random_access_policy():
  access_policy = d1_common.types.generated.dataoneTypes.accessPolicy()
  selected_subjects = {}
  for i in range(random.randint(1, 20)):
    selected_subjects[random.choice(subjects)] = True
  access_rule = d1_common.types.generated.dataoneTypes.AccessRule()
  for selected_subject in selected_subjects.keys():
    access_rule.subject.append(selected_subject)
  permission = d1_common.types.generated.dataoneTypes.Permission('read')
  access_rule.permission.append(permission)
  access_policy.append(access_rule)
  return access_policy


if __name__ == '__main__':
  # Debugging.
  #import pyxb
  #pyxb.RequireValidWhenGenerating(False)

  #print generate_random_sysmeta().toxml()
  print generate_random_access_policy().toxml()
