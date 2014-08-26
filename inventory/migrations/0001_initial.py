# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'inventory_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'inventory', ['Category'])

        # Adding model 'Package'
        db.create_table(u'inventory_package', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'inventory', ['Package'])

        # Adding model 'Part'
        db.create_table(u'inventory_part', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(related_name='parts', to=orm['inventory.Package'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='parts', to=orm['inventory.Category'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'inventory', ['Part'])

        # Adding unique constraint on 'Part', fields ['number', 'package']
        db.create_unique(u'inventory_part', ['number', 'package_id'])

        # Adding M2M table for field bins on 'Part'
        m2m_table_name = db.shorten_name(u'inventory_part_bins')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('part', models.ForeignKey(orm[u'inventory.part'], null=False)),
            ('bin', models.ForeignKey(orm[u'inventory.bin'], null=False))
        ))
        db.create_unique(m2m_table_name, ['part_id', 'bin_id'])

        # Adding model 'Bin'
        db.create_table(u'inventory_bin', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('quantity', self.gf('django.db.models.fields.CharField')(default='empty', max_length=32)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'inventory', ['Bin'])


    def backwards(self, orm):
        # Removing unique constraint on 'Part', fields ['number', 'package']
        db.delete_unique(u'inventory_part', ['number', 'package_id'])

        # Deleting model 'Category'
        db.delete_table(u'inventory_category')

        # Deleting model 'Package'
        db.delete_table(u'inventory_package')

        # Deleting model 'Part'
        db.delete_table(u'inventory_part')

        # Removing M2M table for field bins on 'Part'
        db.delete_table(db.shorten_name(u'inventory_part_bins'))

        # Deleting model 'Bin'
        db.delete_table(u'inventory_bin')


    models = {
        u'inventory.bin': {
            'Meta': {'ordering': "['number']", 'object_name': 'Bin'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'quantity': ('django.db.models.fields.CharField', [], {'default': "'empty'", 'max_length': '32'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'inventory.category': {
            'Meta': {'ordering': "['name']", 'object_name': 'Category'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'inventory.package': {
            'Meta': {'ordering': "['name']", 'object_name': 'Package'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'inventory.part': {
            'Meta': {'ordering': "['number']", 'unique_together': "(('number', 'package'),)", 'object_name': 'Part'},
            'bins': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'parts'", 'symmetrical': 'False', 'to': u"orm['inventory.Bin']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parts'", 'to': u"orm['inventory.Category']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parts'", 'to': u"orm['inventory.Package']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['inventory']