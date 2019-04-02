from flagappender import flag_appender
import sys

flag_generator = flag_appender.PrependedFlagGenerator("-I")
print( flag_generator.generate( sys.argv[1]) )
