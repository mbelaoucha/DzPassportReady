from urllib import parse, request
import time
import re
import argparse

baseUrl = 'http://www.consulat-nanterre-algerie.fr/passeport-il-pret/'

# temps mort entre deux requêtes au site du consulat. 
attemptTimeout = 0.5 # in seconds

verbose = False

def RequestStatusPage(baseUrl, dossierId):
	postData = parse.urlencode({'dossier': str(dossierId)}).encode()
	url = request.Request(baseUrl, data=postData)
	return request.urlopen(url)

def IsPassportReady(lines):
	return not any("VOTRE PASSEPORT N'EST PAS ENCORE PRET" in l for l in lines)

def IsPassportReady2(lines, dossierId):
	regex = '.*VOTRE PASSEPORT  DONT LE NUMERO DE DOSSIER.+' + str(dossierId) + '.+EST DISPONIBLE AU NIVEAU DU CONSULAT.*'
	return any(re.match(regex, l) != None for l in lines)


def CheckPassportReady(dossierId, dumptHtmlToFile=False):
	p = RequestStatusPage(baseUrl, dossierId)
	lines = [ l.decode('UTF8') for l in p]
	if IsPassportReady(lines) and IsPassportReady2(lines, dossierId):
		if verbose: print("-> dossier trouvé: ", dossierId)
		
		if dumptHtmlToFile:
			filename = 'dossier_{}.html'.format(dossierId)
			if verbose: print('Server response had been saved to file: ', filename)
			with open(filename, 'w') as f:
				for l in lines:
					f.write(l)
		return True
	return False

def CheckPassportList(idList, stopAtFirst=True, dumpToFile=False):
	for id in idList:
		print("dossier # ", id, end='')
		try: 
			ready = CheckPassportReady(id, dumpToFile) 
			print(' -> ', 'prêt' if ready else 'pas encore')
			if ready and stopAtFirst: return
		except KeyboardInterrupt :
			print("arrêté par l'utilisateur")
			break
		except:
			print('une erreur technique est survenue')

		# wait before next attempt
		time.sleep(attemptTimeout)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='')

	parser.add_argument('-id', '--identifiant', type=int, help='identifiant du dossier')
	parser.add_argument('-s', '--scan', type=str, help='Syntax: <id start>, <id end>, [<step>]. Default <step> is 1.')
	parser.add_argument('-sc', '--scan-complet', dest='scan_complet', action='store_true', help='Ne pas arrêter le scan au premier dossier trouvé.')
	parser.add_argument('-to', '--timeout', type=float, default=attemptTimeout, help='Temps mort entre deux requêtes (valeur par défaut = {}ms)'.format(attemptTimeout*1000.0))
	parser.add_argument('-d', '--dump-pages', dest='dump_pages', action='store_true', help='Dump des pages html')
	parser.set_defaults(dump_pages=False)

	args = parser.parse_args()

	attemptTimeout = args.timeout

	if args.identifiant is not None:
		CheckPassportList([ int(args.identifiant) ], True, args.dump_pages)
		pass
	elif args.scan is not None:
		fields = str(args.scan).split(',')
		idStart = int(fields[0])
		idEnd = int(fields[1])-1
		try:
			step = int(fields[2])
		except:
			step = 1

		if idStart > idEnd: step = -step

		CheckPassportList( range(idStart, idEnd, step), not args.scan_complet, args.dump_pages )
	else:
		raise ValueError("Merci de renseigner un numéro de dossier (option '-id' ou '-s')")






