# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Bin.quantity'
        db.delete_column(u'inventory_bin', 'quantity')

        # Adding field 'Part.status'
        db.add_column(u'inventory_part', 'status',
                      self.gf('django.db.models.fields.CharField')(default='present', max_length=32),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Bin.quantity'
        db.add_column(u'inventory_bin', 'quantity',
                      self.gf('django.db.models.fields.CharField')(default='empty', max_length=32),
                      keep_default=False)

        # Deleting field 'Part.status'
        db.delete_column(u'inventory_part', 'status')


    models = {
        u'inventory.bin': {
            'Meta': {'ordering': "['number']", 'object_name': 'Bin'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
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
            'search_index': ('djorm_pgfulltext.fields.VectorField', [], {'default': "''", 'null': 'True', 'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'present'", 'max_length': '32'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['inventory']