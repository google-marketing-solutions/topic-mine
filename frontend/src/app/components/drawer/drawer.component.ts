/***************************************************************************
 *
 *  Copyright 2025 Google Inc.
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      https://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 *
 *  Note that these code samples being shared are not official Google
 *  products and are not formally supported.
 *
 ***************************************************************************/

import { Component, ViewChild } from '@angular/core';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatStepperModule } from '@angular/material/stepper';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { ContentTypeSelectionComponent } from '../content-type-selection/content-type-selection.component';
import { DataSourcesConfigComponent } from '../data-sources-config/data-sources-config.component';
import { DestinationsConfigComponent } from '../destinations-config/destinations-config.component';
import { ContentGenerationConfigComponent } from '../content-generation-config/content-generation-config.component';
import { ExecutionStartedComponent } from '../execution-started/execution-started.component';
import { MatStepper } from '@angular/material/stepper';
import { ContentTypeConfig } from '../content-type-selection/content-type-selection.component'
import { DestinationConfig } from '../destinations-config/destinations-config.component';
import { DataSourcesConfig } from '../data-sources-config/data-sources-config.component';
import { ContentGenerationConfig } from '../content-generation-config/content-generation-config.component'

@Component({
  selector: 'app-drawer',
  standalone: true,
  imports: [
    MatSidenavModule,
    MatStepperModule,
    MatButtonModule,
    MatIconModule,
    ContentTypeSelectionComponent,
    DataSourcesConfigComponent,
    DestinationsConfigComponent,
    ContentGenerationConfigComponent,
    ExecutionStartedComponent,
  ],
  templateUrl: './drawer.component.html',
  styleUrl: './drawer.component.css',
})
export class DrawerComponent {
  @ViewChild('stepper') stepper!: MatStepper;

  isNextButtonCTSDisabled: boolean = true;
  isNextButtonSCDisabled: boolean = true;
  isNextButtonDCDisabled: boolean = true;
  isNextButtonCGCDisabled: boolean = true;

  showSideNav: boolean = true;
  isSendingRequest = false;
  requestFailed = false;
  mustShowSecondTermConfig = false;

  currentView = 'content-type-selection';

  contentTypeSelectionConfig: ContentTypeConfig | null = null;
  dataSourcesConfig: DataSourcesConfig | null = null;
  destinationConfig: DestinationConfig | null = null;
  contentGenerationConfig: ContentGenerationConfig | null = null;

  path: string = '';
  body: any = {};

  previousView() {
    if (this.currentView === 'content-type-selection') {
      console.log('GO BACK HOME'); // TODO: GO BACK HOME
      this.stepper.selectedIndex = 0;
    } else if (this.currentView === 'data-sources-config') {
      this.currentView = 'content-type-selection';
      this.stepper.selectedIndex = 0;
    } else if (this.currentView === 'destinations-config') {
      this.currentView = 'data-sources-config';
      this.stepper.selectedIndex = 1
    } else if (this.currentView === 'content-generation-config') {
      this.currentView = 'destinations-config';
      this.stepper.selectedIndex = 2
    }
  }

  nextView() {
    if (this.currentView === 'content-type-selection') {
      this.currentView = 'data-sources-config';
      this.stepper.selectedIndex = 1;
    } else if (this.currentView === 'data-sources-config') {
      this.currentView = 'destinations-config';
      this.stepper.selectedIndex = 2;
    } else if (this.currentView === 'destinations-config') {
      this.currentView = 'content-generation-config';
      this.stepper.selectedIndex = 3;
    } else if (this.currentView === 'content-generation-config') {
      this.currentView = 'execution-started';
      this.showSideNav = false;
    }
  }

  receiveContentTypeSelection(value: any) {
    this.contentTypeSelectionConfig = value;

    if (this.contentTypeSelectionConfig!.numberOfTerms === 2) {
      this.mustShowSecondTermConfig = true;
    } else {
      this.mustShowSecondTermConfig = false;
    }

    this.nextView();
  }

  receiveDataSourcesConfig(value: any) {
    this.dataSourcesConfig = value;

    this.nextView();
  }

  receiveDestinationConfig(value: any) {
    this.destinationConfig = value;

    this.nextView();
  }

  receiveContentGenerationConfig(value: any) {
    this.contentGenerationConfig = value;

    this.isSendingRequest = true;
    this.requestFailed = false;

    console.log(value);

    this.generateQueryPath();
    this.generateBodyParams();

    console.log('QUERY PATH: ' + this.path)
    console.log('BODY PARAMS: ' + this.body)

    // TODO: SEND REQUEST

    setTimeout(() => {
      const success = Math.random() < 0.1; // 80% success rate for demo

      if (success) {
        this.isSendingRequest = false;
        this.nextView();
      } else {
        this.isSendingRequest = false;
        this.requestFailed = true;
      }

    }, 3000);
  }

  generateQueryPath() {
    console.log('CONTENT TYPE SELECTION CONFIG')
    console.log(this.contentTypeSelectionConfig)
    console.log('DATA SOURCES CONFIG')
    console.log(this.dataSourcesConfig)
    console.log('DESTINATION CONFIG')
    console.log(this.destinationConfig)
    console.log('CONTENT GENERATION CONFIG')
    console.log(this.contentGenerationConfig)
    if (this.destinationConfig!.outputFormat === 'Google Ads') {
      // TODO: check if format is the same for GA and SA360
      this.path += '/content?destination=sa360feed';
    } else if (this.destinationConfig!.outputFormat === 'Search Ads 360') {
      this.path += '/content?destination=sa360feed';
    } else if (this.destinationConfig!.outputFormat === 'Display & Video 360') {
      this.path += '/content?destination=dv360feed';
    }

    if (this.dataSourcesConfig!.firstTermSourceConfig.type === 'Google Sheets') {
      this.path += '&first-term-source=spreadsheet';
    } else if (this.dataSourcesConfig!.firstTermSourceConfig.type === 'BigQuery') {
      this.path += '&first-term-source=big_query';
    } else if (this.dataSourcesConfig!.firstTermSourceConfig.type === 'List of terms') {
      // TODO: IMPLEMENT IN THE BACKEND
      throw new Error('Not implemented in the backend yet');
    }

    if (this.contentTypeSelectionConfig!.numberOfTerms === 2) {
      if (this.dataSourcesConfig!.secondTermSourceConfig.type === 'Google Sheets') {
        this.path += '&second-term-source=spreadsheet';
      } else if (this.dataSourcesConfig!.firstTermSourceConfig.type === 'BigQuery') {
        // TODO: IMPLEMENT IN THE BACKEND
        throw new Error('Not implemented in the backend yet');
      } else if (this.dataSourcesConfig!.firstTermSourceConfig.type === 'Google Trends') {
        this.path += '&second-term-source=google_trends';
      }

      if (this.contentTypeSelectionConfig!.mustFindRelationship)
        this.path += '&must-find-relationship=true';
      else
        this.path += '&must-find-relationship=false';
    }
  }

  generateBodyParams() {
    this.body['num_headlines'] = this.contentGenerationConfig!.numberOfHeadlines;
    this.body['num_descriptions'] = this.contentGenerationConfig!.numberOfDescriptions;

    if (this.dataSourcesConfig!.firstTermSourceConfig.type === 'Google Sheets') {
      this.body['first_term_source_config'] = {
        // Mandatory
        'spreadsheet_id': this.dataSourcesConfig!.firstTermSourceConfig.googleSheetsConfig.spreadsheetId,
        'sheet_name': this.dataSourcesConfig!.firstTermSourceConfig.googleSheetsConfig.sheetName,
        'starting_row': this.dataSourcesConfig!.firstTermSourceConfig.googleSheetsConfig.startingRow,
        'term_column': this.dataSourcesConfig!.firstTermSourceConfig.googleSheetsConfig.termColumn,

        // Optional
        'term_description_column': this.dataSourcesConfig!.firstTermSourceConfig.googleSheetsConfig.descriptionColumn,
        'sku_column': this.dataSourcesConfig!.firstTermSourceConfig.googleSheetsConfig.skuColumn,
        'url_column': this.dataSourcesConfig!.firstTermSourceConfig.googleSheetsConfig.urlColumn,
        'imageUrl_column': this.dataSourcesConfig!.firstTermSourceConfig.googleSheetsConfig.imageUrlColumn,
      }
    } else if (this.dataSourcesConfig!.firstTermSourceConfig.type === 'BigQuery') {
      this.body['first_term_source_config'] = {
        // Mandatory
        'project_id': this.dataSourcesConfig!.firstTermSourceConfig.bigQueryConfig.projectId,
        'dataset': this.dataSourcesConfig!.firstTermSourceConfig.bigQueryConfig.dataset,
        'table': this.dataSourcesConfig!.firstTermSourceConfig.bigQueryConfig.table,
        'term_column': this.dataSourcesConfig!.firstTermSourceConfig.termColumn,

        // Optional
        'term_description_column': this.dataSourcesConfig!.firstTermSourceConfig.bigQueryConfig.descriptionColumn,
        'sku_column': this.dataSourcesConfig!.firstTermSourceConfig.bigQueryConfig.skuColumn,
        'url_column': this.dataSourcesConfig!.firstTermSourceConfig.bigQueryConfig.urlColumn,
        'imageUrl_column': this.dataSourcesConfig!.firstTermSourceConfig.bigQueryConfig.imageUrlColumn,
        'limit': this.dataSourcesConfig!.firstTermSourceConfig.bigQueryConfig.limit ?? 0,
      }
    } else if (this.dataSourcesConfig!.firstTermSourceConfig.type === 'List of terms') {
      // TODO: IMPLEMENT IN THE BACKEND
      throw new Error('Not implemented in the backend yet');
    }

    if (this.dataSourcesConfig!.secondTermSourceConfig.type === 'Google Sheets') {
      this.body['second_term_source_config'] = {
        // Mandatory
        'spreadsheet_id': this.dataSourcesConfig!.secondTermSourceConfig.googleSheetsConfig.spreadsheetId,
        'sheet_name': this.dataSourcesConfig!.secondTermSourceConfig.googleSheetsConfig.sheetName,
        'starting_row': this.dataSourcesConfig!.secondTermSourceConfig.googleSheetsConfig.startingRow,
        'term_column': this.dataSourcesConfig!.secondTermSourceConfig.googleSheetsConfig.termColumn,

        // Optional
        'term_description_column': this.dataSourcesConfig!.secondTermSourceConfig.googleSheetsConfig.descriptionColumn
      }
    } else if (this.dataSourcesConfig!.firstTermSourceConfig.type === 'BigQuery') {
      // TODO: IMPLEMENT IN THE BACKEND
      throw new Error('Not implemented in the backend yet');
    } else if (this.dataSourcesConfig!.firstTermSourceConfig.type === 'Google Trends') {
      this.body['second_term_source_config'] = {
        'limit':this.dataSourcesConfig!.secondTermSourceConfig.googleTrendsConfig.limit
      }
    }

    this.body['destination_config'] = {
      'spreadsheet_id': this.destinationConfig!.spreadsheetId,
      'sheet_name': this.destinationConfig!.sheetName,
    }

    this.body['headlines_blocklist'] = this.contentGenerationConfig!.headlinesBlocklist;
    this.body['headlines_regexp_blocklist'] = this.contentGenerationConfig!.headlinesRegexBlocklist;
    this.body['descriptions_blocklist'] = this.contentGenerationConfig!.headlinesBlocklist;
    this.body['descriptions_regexp_blocklist'] = this.contentGenerationConfig!.descriptionsRegexBlocklist;

    this.body['generic_copies'] = {
      'headlines': this.contentGenerationConfig!.genericHeadlines,
      'descriptions': this.contentGenerationConfig!.genericDescriptions,
    }

    this.body['enable_feature_extraction'] = this.contentGenerationConfig!.enableFeatureExtraction;

    if (this.contentGenerationConfig!.enableURLValidation)
      this.body['enable_url_validation'] = 'REMOVE_BROKEN_URLS'

    // TODO: MUST IMPLEMENT IN THE FRONTEND
    // this.body['default_url'] = this.dataSourcesConfig!.defaultUrl;
    this.body['generate_paths'] = this.contentGenerationConfig!.generatePaths;

    // TODO: MUST IMPLEMENT IN THE BACKEND ALL OF THE FOLLOWING
    this.body['generate_keywords'] = this.contentGenerationConfig!.generateKeywords;
    this.body['advertiser_name'] = this.contentGenerationConfig!.advertiserName;
    this.body['country'] = this.contentGenerationConfig!.country;
    this.body['gemini_model'] = this.contentGenerationConfig!.geminiModel;
    this.body['language'] = this.contentGenerationConfig!.language;
  }


  receiveNextButtonDisabledEvent(value: boolean) {
    switch(this.currentView) {
      case 'content-type-selection':
        this.isNextButtonCTSDisabled = value;
        break;
      case 'data-sources-config':
        this.isNextButtonSCDisabled = value;
        break;
      case 'destinations-config':
        this.isNextButtonDCDisabled = value;
        break;
      case 'content-generation-config':
        this.isNextButtonCGCDisabled = value;
        break;
    }
  }
}
