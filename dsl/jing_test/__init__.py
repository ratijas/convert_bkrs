#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import subprocess, os

def run( filename ):
	dirpath = os.path.dirname(__file__) + '/'

	jing_jar_path	= dirpath + 'jing/bin/jing.jar'
	rng_path		= dirpath + 'DictionarySchema/AppleDictionarySchema.rng'
	pipe = None
	args = [ 'java', '-Xmx4G', '-jar', jing_jar_path, rng_path, filename ]

	print u'запускаю `jing` тест:\n' '%s\n...' % u' '.join( args )
	pipe = subprocess.Popen(
		args,
		stdout=subprocess.PIPE )
	retcode = pipe.wait()
	try:
		if retcode is not 0:
			if retcode < 0:
				print u'`jing` тест был завершен сигналом %d' % -retcode
			elif  retcode > 0:
				print u'`jing` вернул %d' % retcode
			raise Exception( '`jing` тест завалился :(' )

	except:
		print '%s' % pipe.communicate()[ 0 ]
		raise
	else:
		print '`jing` тест успешно пройден!!! ;)'
