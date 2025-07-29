"""
Miva Merchant

This file and the source codes contained herein are the property of
Miva, Inc.  Use of this file is restricted to the specific terms and
conditions in the License Agreement associated with this file.  Distribution
of this file or portions of this file for uses not covered by the License
Agreement is not allowed without a written agreement signed by an officer of
Miva, Inc.

Copyright 1998-2025 Miva, Inc.  All rights reserved.
https://www.miva.com

Prefix         : MMT-COMMAND-SRI-
Next Error Code: 4
"""

import typing
import hashlib

from mmt.exceptions import Error
from mmt.commands import ConfiguredCommand


class SRICommand( ConfiguredCommand ):
	def __init__( self, *args, **kwargs ):
		super().__init__( *args, **kwargs )

		self._local_resource_files	= []
		self._algorithms			= [ 'sha256', 'sha384', 'sha512' ] # Default SRI algorithms

	def validate( self ):
		for filepath in self.args.get( 'filepaths' ):
			state_file = self.state.filemanager.lookup( filepath )

			if state_file is None:
				raise Error( 'MMT-COMMAND-SRI-00001', f'File \'{filepath}\' does not exist' )

			if not state_file.is_jsresource_js_file() and not state_file.is_cssresource_css_file():
				raise Error( 'MMT-COMMAND-SRI-00002', f'File \'{filepath}\' is not a local resource' )

	def initialize( self ):
		# Determine the SRI algorithms
		if self.args.get( 'sha256' ) or self.args.get( 'sha384' ) or self.args.get( 'sha512' ):
			self._algorithms.clear()

			if self.args.get( 'sha256' ):
				self._algorithms.append( 'sha256' )

			if self.args.get( 'sha384' ):
				self._algorithms.append( 'sha384' )

			if self.args.get( 'sha512' ):
				self._algorithms.append( 'sha512' )

		# Determine which resources to operate on
		filepaths = []

		if len( self.args.get( 'filepaths' ) ) > 0:
			filepaths = list( set( self.args.get( 'filepaths' ) ) ) # Force the user supplied filepaths to be unique
		else:
			for state_file in self.state.filemanager.files:
				# Process all local JS and CSS resources
				if state_file.is_jsresource_js_file() or state_file.is_cssresource_css_file():
					filepaths.append( state_file.filepath )

		# Find the local settings files for each filepath
		for filepath in filepaths:
			local_source_state_file		= self.state.filemanager.lookup( filepath )
			local_settings_state_file	= None

			# Find the local settings file
			for state_file in self.state.filemanager.files:
				if local_source_state_file.is_jsresource_js_file() and state_file.is_jsresource_settings_file() and local_source_state_file.jsresource_code == state_file.jsresource_code:
					local_settings_state_file = state_file
					break
				elif local_source_state_file.is_cssresource_css_file() and state_file.is_cssresource_settings_file() and local_source_state_file.cssresource_code == state_file.cssresource_code:
					local_settings_state_file = state_file
					break

			if local_settings_state_file is None:
				raise Error( 'MMT-COMMAND-SRI-00003', f'Failed to find the local settings file associated with \'{filepath}\'' )

			self._local_resource_files.append( ( local_source_state_file.filepath, local_settings_state_file.filepath ) )

	def run( self ):
		for local_source_filepath, local_settings_filepath in self._local_resource_files:
			integrity_attribute		= { 'name': 'integrity',	'value': self._generate_sri_value( local_source_filepath ) }
			crossorigin_attribute	= { 'name': 'crossorigin',	'value': 'anonymous' }

			# Load the existing settings
			with open( local_settings_filepath, 'r' ) as fh:
				settings = self.json_loads( fh.read() )

			# Search for an existing crossorigin attribute and use that if it exists
			for attribute in settings[ 'attributes' ]:
				if attribute[ 'name' ].lower() == 'crossorigin':
					crossorigin_attribute = attribute
					break

			# Filter out existing integrity and crossorigin attributes
			attributes = [ attribute for attribute in settings[ 'attributes' ] if attribute[ 'name' ].lower() not in [ 'integrity', 'crossorigin' ] ]
			attributes.append( integrity_attribute )
			attributes.append( crossorigin_attribute )

			settings[ 'attributes' ] = attributes

			# Write the new settings
			with open( local_settings_filepath, 'w' ) as fh:
				fh.write( self.json_dumps( settings ) )

	def _generate_sri_value( self, filepath: str ) -> str:
		hash_objects = {}

		for algorithm in self._algorithms:
			hash_objects[ algorithm ] = hashlib.new( algorithm )

		with open( filepath, 'rb' ) as fh:
			for block in iter( lambda: fh.read( 4096 ), b'' ):
				for hash_object in hash_objects.values():
					hash_object.update( block )

		return ' '.join( [ f'{algorithm}-{self.base64_encode( hash_object.digest() ).decode( "ascii" )}' for algorithm, hash_object in hash_objects.items() ] )
