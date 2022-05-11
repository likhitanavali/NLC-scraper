import pg_import_creator


def main():
  tv_dir = 'D:\\Spring22\\RA\\nlc-script-database-master\\scraper\\test\\tv-series'
  movie_dir = 'D:\\Spring22\\RA\\nlc-script-database-master\\scraper\\test\\movies'
  print('Starting import file creation')

  try:
    import_creator = pg_import_creator.PostgressImportCreator(tv_dir, movie_dir)
    import_creator.create_import_files()
    print('Import file creation finished. Please check log files.')
  except Exception as e:
    print('An error occurred during the import file creation process: {error}'.format(error=str(e)))


if __name__ == '__main__':
  main()
