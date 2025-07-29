import os
import typing

from mmt.exceptions import Error
from test import MMTTest


class Test( MMTTest ):
	def test_sri_validate_errors( self ):
		def validate_error_filepath( filepath: str ):
			with self.assertRaises( Error ) as e:
				self.sri( filepaths = [ filepath ] )

			self.assertEqual( e.exception.error_message, f'File \'{filepath}\' is not a local resource' )

		self.import_store_provisioning_file( 'test_sri_validate_errors.xml' )
		self.checkout()

		# File does not exist
		with self.assertRaises( Error ) as e:
			self.sri( filepaths = [ 'test_sri_validate_errors.txt' ] )

		self.assertEqual( e.exception.error_message, 'File \'test_sri_validate_errors.txt\' does not exist' )

		# Validate non-local source resource files generate the expected error
		validate_error_filepath( self.template_path( 'test_sri_validate_errors.mvt' ) )
		validate_error_filepath( self.template_path( 'test_sri_validate_errors.json' ) )
		validate_error_filepath( self.property_path( 'readytheme_contentsection', 'test_sri_validate_errors.mvt' ) )
		validate_error_filepath( self.property_path( 'readytheme_contentsection', 'test_sri_validate_errors.json' ) )
		validate_error_filepath( self.jsresource_path( 'test_sri_validate_errors_inline.mvt' ) )
		validate_error_filepath( self.jsresource_path( 'test_sri_validate_errors_inline.json' ) )
		validate_error_filepath( self.jsresource_path( 'test_sri_validate_errors_local.json' ) )
		validate_error_filepath( self.cssresource_path( 'test_sri_validate_errors_inline.mvt' ) )
		validate_error_filepath( self.cssresource_path( 'test_sri_validate_errors_inline.json' ) )
		validate_error_filepath( self.cssresource_path( 'test_sri_validate_errors_local.json' ) )

	def test_sri_initialize_errors( self ):
		self.import_store_provisioning_file( 'test_sri_initialize_errors.xml' )
		self.checkout()

		state_filepath = os.path.join( '.mmt', 'state.json' )

		with open( state_filepath ) as fh:
			state_file = self.json_loads( fh.read() )

		del state_file[ 'files' ][ self.jsresource_path( 'test_sri_initialize_errors.json' ) ]

		with open( state_filepath, 'w' ) as fh:
			fh.write( self.json_dumps( state_file ) )

		with self.assertRaises( Error ) as e:
			self.sri( filepaths = [ self.jsresource_path( 'test_sri_initialize_errors.js' ) ] )

		self.assertEqual( e.exception.error_message, f'Failed to find the local settings file associated with \'{ self.jsresource_path( "test_sri_initialize_errors.js" ) }\'' )

	def test_sri_filepaths( self ):
		self.import_store_provisioning_file( 'test_sri_filepaths.xml' )
		self.checkout()

		status = self.status()
		self.assertEqual( status, 'No files modified' )

		# Specific filepaths only
		self.sri( filepaths = [ self.jsresource_path( 'test_sri_filepaths_1.js' ), self.cssresource_path( 'test_sri_filepaths_2.css' ) ] )

		status = self.status()

		self.assertIn( self.jsresource_path( 'test_sri_filepaths_1.json' ),		status )
		self.assertIn( self.cssresource_path( 'test_sri_filepaths_2.json' ),	status )

		self.assertNotIn( self.jsresource_path( 'test_sri_filepaths_2.json' ),	status )
		self.assertNotIn( self.cssresource_path( 'test_sri_filepaths_1.json' ),	status )

		# Revert files
		self.revert( _all = True )

		# All filepaths
		self.sri( filepaths = [] )

		status = self.status()

		self.assertIn( self.jsresource_path( 'test_sri_filepaths_1.json' ),		status )
		self.assertIn( self.jsresource_path( 'test_sri_filepaths_2.json' ),		status )
		self.assertIn( self.cssresource_path( 'test_sri_filepaths_1.json' ),	status )
		self.assertIn( self.cssresource_path( 'test_sri_filepaths_2.json' ),	status )

	def test_sri_all_algorithms( self ):
		js_upload_filepath	= self.upload_js_file_from_data( 'test_sri_all_algorithms.js', 'console.log( \'test_sri_all_algorithms\' )' ).json().get( 'data' ).get( 'file_path' )
		css_upload_filepath	= self.upload_css_file_from_data( 'test_sri_all_algorithms.css', '.test_sri_all_algorithms { display: block; }' ).json().get( 'data' ).get( 'file_path' )

		self.import_store_provisioning_file( 'test_sri_all_algorithms.xml', [ ( '%test_sri_all_algorithms.js%', js_upload_filepath ), ( '%test_sri_all_algorithms.css%', css_upload_filepath ) ] )
		self.checkout()

		self.sri( algorithms = [], filepaths = [ self.jsresource_path( 'test_sri_all_algorithms.js' ), self.cssresource_path( 'test_sri_all_algorithms.css' ) ] )

		with self.jsresource_open( 'test_sri_all_algorithms.json' ) as fh:
			self.assertSettingsEqual( fh.read(),
			{
				'attributes':
				[
					{ 'name': 'integrity',		'value': 'sha256-nt+NeCiZOLYYvhae5NBHo1VSqdQE6bSJe/yHBM0gCvg= sha384-FmjnM78//NrykbAsuaO66fKX/0ct2ZTCqaKF4IkB6xKeaB5g2g1gW8Sbt6vQojXN sha512-meymrHnSIpvhPC9PhY6HFubYvrKuwaFZQelmupeg109Aiy+65he29X34k0lIIKGb+2lqy+xgIx4c7Z3Vq1/q9Q==' },
					{ 'name': 'crossorigin',	'value': 'anonymous' }
				]
			} )

		with self.cssresource_open( 'test_sri_all_algorithms.json' ) as fh:
			self.assertSettingsEqual( fh.read(),
			{
				'attributes':
				[
					{ 'name': 'integrity',		'value': 'sha256-ZDDjRa7I6HaL8Fw3gQMA+M+gxBmaQQNbi/y1CT3IzwU= sha384-ULYket/Pgr1nPHL5HDUo8fJTisBcDOPP+HuOdHDgDXjv440X5pxp+cLQ8QvfBpTR sha512-BcRyPtNL6dP7dwQfI3FGcKsOkDjoLAmbkCoNzw+mQSkLlAYrt/LH+8Fo2PmurwkMPVsm6lVxZ7IGiUWWiNlnxQ==' },
					{ 'name': 'crossorigin',	'value': 'anonymous' }
				]
			} )

	def test_sri_all_algorithms_explicit( self ):
		js_upload_filepath	= self.upload_js_file_from_data( 'test_sri_all_algorithms_explicit.js', 'console.log( \'test_sri_all_algorithms_explicit\' )' ).json().get( 'data' ).get( 'file_path' )
		css_upload_filepath	= self.upload_css_file_from_data( 'test_sri_all_algorithms_explicit.css', '.test_sri_all_algorithms_explicit { display: block; }' ).json().get( 'data' ).get( 'file_path' )

		self.import_store_provisioning_file( 'test_sri_all_algorithms_explicit.xml', [ ( '%test_sri_all_algorithms_explicit.js%', js_upload_filepath ), ( '%test_sri_all_algorithms_explicit.css%', css_upload_filepath ) ] )
		self.checkout()

		self.sri( algorithms = [ 'sha256', 'sha384', 'sha512' ], filepaths = [ self.jsresource_path( 'test_sri_all_algorithms_explicit.js' ), self.cssresource_path( 'test_sri_all_algorithms_explicit.css' ) ] )

		with self.jsresource_open( 'test_sri_all_algorithms_explicit.json' ) as fh:
			self.assertSettingsEqual( fh.read(),
			{
				'attributes':
				[
					{ 'name': 'integrity',		'value': 'sha256-6Bk3jWIuIgEgPDxKTEqQpxOIFr0aQORMwKHDxi88eDM= sha384-4nGOxXm5lgJ+J0qESOnYE7Iw/6OuXo/rgX5QePOGxeEu5xGkS5AHhqkmkxqgLHUC sha512-rnsQHdklSdTRjk8SuLM9liQLH+uh9/CddXq/3xXj/G/MCdBMvYueqPlDkY4h/1hvFZvdmDtWc7vcoFYWS3aQKA==' },
					{ 'name': 'crossorigin',	'value': 'anonymous' }
				]
			} )

		with self.cssresource_open( 'test_sri_all_algorithms_explicit.json' ) as fh:
			self.assertSettingsEqual( fh.read(),
			{
				'attributes':
				[
					{ 'name': 'integrity',		'value': 'sha256-WUsEF7eotU3bMoYgliu1WeFi7T/kDOH2ZF7RcRln4Ys= sha384-bKEzFn+3k9a8GHLc/SnhB1VXrYGZqFyMKBHNWvnZmICK+f9o5CTk6PRg+IkJl7ty sha512-JcPWtDesk4WxOKNLuvaoijsCv4qrNV6B5oPBuzA5kUIZrxMGE1BuVCKJFLoy0OM/iFUzCG0JTsfkavgLmt5ipQ==' },
					{ 'name': 'crossorigin',	'value': 'anonymous' }
				]
			} )

	def test_sri_specific_algorithms( self ):
		js_upload_filepath	= self.upload_js_file_from_data( 'test_sri_specific_algorithms.js', 'console.log( \'test_sri_specific_algorithms\' )' ).json().get( 'data' ).get( 'file_path' )
		css_upload_filepath	= self.upload_css_file_from_data( 'test_sri_specific_algorithms.css', '.test_sri_specific_algorithms { display: block; }' ).json().get( 'data' ).get( 'file_path' )

		self.import_store_provisioning_file( 'test_sri_specific_algorithms.xml', [ ( '%test_sri_specific_algorithms.js%', js_upload_filepath ), ( '%test_sri_specific_algorithms.css%', css_upload_filepath ) ] )
		self.checkout()

		self.sri( algorithms = [ 'sha256' ], filepaths = [ self.jsresource_path( 'test_sri_specific_algorithms.js' ) ] )

		with self.jsresource_open( 'test_sri_specific_algorithms.json' ) as fh:
			self.assertSettingsEqual( fh.read(),
			{
				'attributes':
				[
					{ 'name': 'integrity',		'value': 'sha256-H/dC+H/cfnVyfbnZy4ZkAsD0bFVlOTJqoOyZLYIY5ao=' },
					{ 'name': 'crossorigin',	'value': 'anonymous' }
				]
			} )

		self.sri( algorithms = [ 'sha384', 'sha512' ], filepaths = [ self.cssresource_path( 'test_sri_specific_algorithms.css' ) ] )

		with self.cssresource_open( 'test_sri_specific_algorithms.json' ) as fh:
			self.assertSettingsEqual( fh.read(),
			{
				'attributes':
				[
					{ 'name': 'integrity',		'value': 'sha384-2OQcpjGiLBFu55UlQsVH1ZZTUSOWQlpBdGM+5lI+AY86GbjxwE/33DEH/vizkwIx sha512-cSwAtO0wDwde7Rx5fGlJ8sGn+GOPyYMSzihIGhoHcCSU2S1wThT6JWXW4Rvsx3+98EdWgqT9Q6TUIwsCLXDWug==' },
					{ 'name': 'crossorigin',	'value': 'anonymous' }
				]
			} )

	def test_sri_attributes( self ):
		js_upload_filepath	= self.upload_js_file_from_data( 'test_sri_attributes.js', 'console.log( \'test_sri_attributes\' )' ).json().get( 'data' ).get( 'file_path' )
		css_upload_filepath	= self.upload_css_file_from_data( 'test_sri_attributes.css', '.test_sri_attributes { display: block; }' ).json().get( 'data' ).get( 'file_path' )

		self.import_store_provisioning_file( 'test_sri_attributes.xml', [ ( '%test_sri_attributes.js%', js_upload_filepath ), ( '%test_sri_attributes.css%', css_upload_filepath ) ] )
		self.checkout()

		self.sri( algorithms = [ 'sha512' ], filepaths = [ self.jsresource_path( 'test_sri_attributes.js' ), self.cssresource_path( 'test_sri_attributes.css' ) ] )

		with self.jsresource_open( 'test_sri_attributes.json' ) as fh:
			self.assertSettingsEqual( fh.read(),
			{
				'attributes':
				[
					{ 'name': 'random',			'value': 'This should not be modified' },
					{ 'name': 'integrity',		'value': 'sha512-z4PhNX7vuL3xVChQ1m2AB9Yg5AULVxXcg/SpIdNs6c5H0NE8XYXysP+DGNKHfuwvY7kxvUdBeoGlODJ6+SfaPg==' },
					{ 'name': 'CroSSoriGin',	'value': 'This should not be modified' }
				]
			} )

		with self.cssresource_open( 'test_sri_attributes.json' ) as fh:
			self.assertSettingsEqual( fh.read(),
			{
				'attributes':
				[
					{ 'name': 'integrity',		'value': 'sha512-z4PhNX7vuL3xVChQ1m2AB9Yg5AULVxXcg/SpIdNs6c5H0NE8XYXysP+DGNKHfuwvY7kxvUdBeoGlODJ6+SfaPg==' },
					{ 'name': 'crossorigin',	'value': 'anonymous' }
				]
			} )

	def test_sri_generic( self ):
		js_upload_filepath	= self.upload_js_file_from_data( 'test_sri_generic.js', 'console.log( \'test_sri_generic\' )' ).json().get( 'data' ).get( 'file_path' )
		css_upload_filepath	= self.upload_css_file_from_data( 'test_sri_generic.css', '.test_sri_generic { display: block; }' ).json().get( 'data' ).get( 'file_path' )

		self.import_store_provisioning_file( 'test_sri_generic.xml', [ ( '%test_sri_generic.js%', js_upload_filepath ), ( '%test_sri_generic.css%', css_upload_filepath ) ] )
		self.checkout()

		with self.jsresource_open( 'test_sri_generic.json' ) as fh:
			js_settings_before = self.json_loads( fh.read() )

		with self.cssresource_open( 'test_sri_generic.json' ) as fh:
			css_settings_before = self.json_loads( fh.read() )

		self.sri( algorithms = [ 'sha384' ], filepaths = [ self.jsresource_path( 'test_sri_generic.js' ), self.cssresource_path( 'test_sri_generic.css' ) ] )

		# Commit the changes
		self.push( 'test_sri_generic' )

		# Verify the files are no longer locally modified
		status = self.status()
		self.assertEqual( status, 'No files modified' )

		# Checkout out again and verify the settings match as expected
		self.checkout()

		with self.jsresource_open( 'test_sri_generic.json' ) as fh:
			js_settings_after = self.json_loads( fh.read() )

			self.assertSettingsEqual( js_settings_after,
			{
				'attributes':
				[
					{ 'name': 'integrity',		'value': 'sha384-v2VGOqS3aOTC3Zo9JhRYp77pDQIpprB8hsW1/PlpHhDj3d7tlNi04enpkqP+euO7' },
					{ 'name': 'crossorigin',	'value': 'anonymous' }
				]
			} )

			# Clear the attributes and compare the files to make sure they are the same and to ensure generating the SRI did not modify any other values
			js_settings_after[ 'attributes' ].clear()
			self.assertSettingsEqual( js_settings_after, js_settings_before )

		with self.cssresource_open( 'test_sri_generic.json' ) as fh:
			css_settings_after = self.json_loads( fh.read() )

			self.assertSettingsEqual( css_settings_after,
			{
				'attributes':
				[
					{ 'name': 'integrity',		'value': 'sha384-ntw4WDlnplYYuMsmhBdSjbOS6v+kmn39sGV/dVQ/1cqqH64SpVF1J8/ZWFjnMbW8' },
					{ 'name': 'crossorigin',	'value': 'anonymous' }
				]
			} )

			# Clear the attributes and compare the files to make sure they are the same and to ensure generating the SRI did not modify any other values
			css_settings_after[ 'attributes' ].clear()
			self.assertSettingsEqual( css_settings_after, css_settings_before )
