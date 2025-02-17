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

import { Component, Input } from '@angular/core';
import {
  FormControl,
  FormGroupDirective,
  NgForm,
  Validators,
  FormsModule,
  ReactiveFormsModule,
} from '@angular/forms';
import { Output, EventEmitter } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatDividerModule } from '@angular/material/divider';
import { MatIconModule } from '@angular/material/icon';
import { MatTabsModule } from '@angular/material/tabs';
import { ErrorStateMatcher } from '@angular/material/core';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatTooltipModule } from '@angular/material/tooltip';

/** Error when invalid control is dirty, touched, or submitted. */
export class MyErrorStateMatcher implements ErrorStateMatcher {
  isErrorState(control: FormControl | null, form: FormGroupDirective | NgForm | null): boolean {
    const isSubmitted = form && form.submitted;
    return !!(control && control.invalid && (control.dirty || control.touched || isSubmitted));
  }
}

export interface DataSourcesConfig {
  firstTermSourceConfig: any;
  secondTermSourceConfig?: any;
}

// Custom integer validator function
export function integerValidator(): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    const value = control.value;
    if (value === null || value === '') {
      return null; // Don't validate empty values
    }
    const isValid = Number.isInteger(Number(value));
    return isValid ? null : { integer: true };
  };
}


@Component({
  selector: 'app-data-sources-config',
  standalone: true,
  imports: [FormsModule, ReactiveFormsModule, MatButtonModule, MatDividerModule, MatFormFieldModule, MatGridListModule, MatIconModule, MatInputModule, MatTabsModule, MatTooltipModule],
  templateUrl: './data-sources-config.component.html',
  styleUrl: './data-sources-config.component.css',
})
export class DataSourcesConfigComponent {
  @Input() mustShowSecondTermConfig: boolean = false;

  @Output() dataSourcesConfigEvent = new EventEmitter<DataSourcesConfig>();
  @Output() changeViewEvent = new EventEmitter<string>();
  @Output() nextButtonDisabledEvent = new EventEmitter<boolean>();


  // Required Google Sheets first term fields
  spreadsheetIdGoogleSheetsFirstTermFormControl = new FormControl('', [Validators.required, Validators.nullValidator]);
  sheetNameGoogleSheetsFirstTermFormControl = new FormControl('', [Validators.required, Validators.nullValidator]);
  termColumnGoogleSheetsFirstTermFormControl = new FormControl('', [Validators.required, Validators.nullValidator]);
  startingRowGoogleSheetsFirstTermFormControl = new FormControl('', [Validators.required, Validators.min(1), integerValidator()]);
  limitGoogleSheetsFirstTermFormControl = new FormControl('', [Validators.required, Validators.min(1), integerValidator()]);
  // Optional Google Sheets first term fields
  descriptionColumnGoogleSheetsFirstTermFormControl = new FormControl('', []);
  skuColumnGoogleSheetsFirstTermFormControl = new FormControl('', []);
  urlColumnGoogleSheetsFirstTermFormControl = new FormControl('', []);
  imageUrlColumnGoogleSheetsFirstTermFormControl = new FormControl('', []);

  // Required BigQuery first term fields
  projectIdBigQueryFirstTermFormControl = new FormControl('', [Validators.required, Validators.nullValidator]);
  datasetBigQueryFirstTermFormControl = new FormControl('', [Validators.required, Validators.nullValidator]);
  tableBigQueryFirstTermFormControl = new FormControl('', [Validators.required, Validators.nullValidator]);
  termColumnBigQueryFirstTermFormControl = new FormControl('', [Validators.required, Validators.nullValidator]);
  // Optional BigQuery first term fields
  descriptionColumnBigQueryFirstTermFormControl = new FormControl('', []);
  skuColumnBigQueryFirstTermFormControl = new FormControl('', []);
  urlColumnBigQueryFirstTermFormControl = new FormControl('', []);
  imageUrlColumnBigQueryFirstTermFormControl = new FormControl('', []);
  limitBigQueryFirstTermFormControl = new FormControl('', [Validators.min(1), integerValidator()]);

  // Required list of terms first term fields
  listOfTermsFirstTermFormControl = new FormControl('', [Validators.required, Validators.nullValidator]);



  // Required Google Sheets second term fields
  spreadsheetIdGoogleSheetsSecondTermFormControl = new FormControl('', [Validators.required, Validators.nullValidator]);
  sheetNameGoogleSheetsSecondTermFormControl = new FormControl('', [Validators.required, Validators.nullValidator]);
  termColumnGoogleSheetsSecondTermFormControl = new FormControl('', [Validators.required, Validators.nullValidator]);
  startingRowGoogleSheetsSecondTermFormControl = new FormControl('', [Validators.required, Validators.min(1), integerValidator()]);
  limitGoogleSheetsSecondTermFormControl = new FormControl('', [Validators.required, Validators.min(1), integerValidator()]);
  // Optional Google Sheets second term fields
  descriptionColumnGoogleSheetsSecondTermFormControl = new FormControl('', []);

  // Required BigQuery second term fields
  projectIdBigQuerySecondTermFormControl = new FormControl('', [Validators.required, Validators.nullValidator]);
  datasetBigQuerySecondTermFormControl = new FormControl('', [Validators.required, Validators.nullValidator]);
  tableBigQuerySecondTermFormControl = new FormControl('', [Validators.required, Validators.nullValidator]);
  termColumnBigQuerySecondTermFormControl = new FormControl('', [Validators.required, Validators.nullValidator]);
  // Optional BigQuery second term fields
  descriptionColumnBigQuerySecondTermFormControl = new FormControl('', []);
  limitBigQuerySecondTermFormControl = new FormControl('', [Validators.min(1), integerValidator()]);

  // Optional Google Trends second term fields
  limitGoogleTrendsSecondTermFormControl = new FormControl('', [Validators.min(1), integerValidator()]);



  matcher = new MyErrorStateMatcher();

  firstTermSourceSelected: string = 'Google Sheets first term';
  secondTermSourceSelected: string = 'Google Sheets second term';

  isNextButtonDisabled: boolean = true;

  ngOnInit() {
    // FIRST TERM, GOOGLE SHEETS
    this.spreadsheetIdGoogleSheetsFirstTermFormControl.valueChanges.subscribe(() => this.updateNextButtonState());
    this.sheetNameGoogleSheetsFirstTermFormControl.valueChanges.subscribe(() => this.updateNextButtonState());
    this.termColumnGoogleSheetsFirstTermFormControl.valueChanges.subscribe(() => this.updateNextButtonState());
    this.startingRowGoogleSheetsFirstTermFormControl.valueChanges.subscribe(() => this.updateNextButtonState());
    this.limitGoogleSheetsFirstTermFormControl.valueChanges.subscribe(() => this.updateNextButtonState());
    // FIRST TERM, BIG QUERY
    this.projectIdBigQueryFirstTermFormControl.valueChanges.subscribe(() => this.updateNextButtonState());
    this.datasetBigQueryFirstTermFormControl.valueChanges.subscribe(() => this.updateNextButtonState());
    this.tableBigQueryFirstTermFormControl.valueChanges.subscribe(() => this.updateNextButtonState());
    this.termColumnBigQueryFirstTermFormControl.valueChanges.subscribe(() => this.updateNextButtonState());
    // FIRST TERM, LIST OF TERMS
    this.listOfTermsFirstTermFormControl.valueChanges.subscribe(() => this.updateNextButtonState());
    // SECOND TERM, GOOGLE SHEETS
    this.spreadsheetIdGoogleSheetsSecondTermFormControl.valueChanges.subscribe(() => this.updateNextButtonState());
    this.sheetNameGoogleSheetsSecondTermFormControl.valueChanges.subscribe(() => this.updateNextButtonState());
    this.termColumnGoogleSheetsSecondTermFormControl.valueChanges.subscribe(() => this.updateNextButtonState());
    this.startingRowGoogleSheetsSecondTermFormControl.valueChanges.subscribe(() => this.updateNextButtonState());
    this.limitGoogleSheetsSecondTermFormControl.valueChanges.subscribe(() => this.updateNextButtonState());
    // SECOND TERM, BIG QUERY
    this.projectIdBigQuerySecondTermFormControl.valueChanges.subscribe(() => this.updateNextButtonState());
    this.datasetBigQuerySecondTermFormControl.valueChanges.subscribe(() => this.updateNextButtonState());
    this.tableBigQuerySecondTermFormControl.valueChanges.subscribe(() => this.updateNextButtonState());
    this.termColumnBigQuerySecondTermFormControl.valueChanges.subscribe(() => this.updateNextButtonState());
  }

  onFirstTermTabSelected(label: string) {
    this.firstTermSourceSelected = label;
    this.updateNextButtonState();
  }

  onSecondTermTabSelected(label: string) {
    this.secondTermSourceSelected = label;
    this.updateNextButtonState();
  }

  firstTermFormValid() {
    return (
        this.firstTermSourceSelected === 'Google Sheets first term' &&
        this.spreadsheetIdGoogleSheetsFirstTermFormControl.valid &&
        this.sheetNameGoogleSheetsFirstTermFormControl.valid &&
        this.termColumnGoogleSheetsFirstTermFormControl.valid &&
        this.startingRowGoogleSheetsFirstTermFormControl.valid &&
        this.limitGoogleSheetsFirstTermFormControl.valid
      ) || (
        this.firstTermSourceSelected === 'BigQuery first term' &&
        this.projectIdBigQueryFirstTermFormControl.valid &&
        this.datasetBigQueryFirstTermFormControl.valid &&
        this.tableBigQueryFirstTermFormControl.valid &&
        this.termColumnBigQueryFirstTermFormControl.valid
      ) || (
        this.firstTermSourceSelected === 'List of terms first term' &&
        this.listOfTermsFirstTermFormControl.valid
      )
  }

  secondTermFormValid() {
    if (!this.mustShowSecondTermConfig) return true;

    return (
        this.secondTermSourceSelected === 'Google Sheets second term' &&
        this.mustShowSecondTermConfig === true &&
        this.spreadsheetIdGoogleSheetsSecondTermFormControl.valid &&
        this.sheetNameGoogleSheetsSecondTermFormControl.valid &&
        this.termColumnGoogleSheetsSecondTermFormControl.valid &&
        this.startingRowGoogleSheetsSecondTermFormControl.valid &&
        this.limitGoogleSheetsSecondTermFormControl.valid
      ) || (
        this.secondTermSourceSelected === 'BigQuery second term' &&
        this.mustShowSecondTermConfig === true &&
        this.projectIdBigQuerySecondTermFormControl.valid &&
        this.datasetBigQuerySecondTermFormControl.valid &&
        this.tableBigQuerySecondTermFormControl.valid &&
        this.termColumnBigQuerySecondTermFormControl.valid
      ) || (
        this.secondTermSourceSelected === 'Google Trends second term' &&
        this.mustShowSecondTermConfig === true
      )
  }

  updateNextButtonState() {
    if (this.firstTermFormValid() && this.secondTermFormValid()) {
      this.isNextButtonDisabled = false;
      this.nextButtonDisabledEvent.emit(false);
      return;
    }

    this.isNextButtonDisabled = true;
    this.nextButtonDisabledEvent.emit(true);
  }


  goBack() {
    this.changeViewEvent.emit('content-type-selection');
  }

  sendDataSourcesConfig() {
    const config: DataSourcesConfig = {
      firstTermSourceConfig: {
        type: this.firstTermSourceSelected.replace(' first term', ''),
        googleSheetsConfig: {
          spreadsheetId: this.spreadsheetIdGoogleSheetsFirstTermFormControl.value,
          sheetName: this.sheetNameGoogleSheetsFirstTermFormControl.value,
          termColumn: this.termColumnGoogleSheetsFirstTermFormControl.value,
          startingRow: Number(this.startingRowGoogleSheetsFirstTermFormControl.value),
          limit: Number(this.limitGoogleSheetsFirstTermFormControl.value),
          descriptionColumn: this.descriptionColumnGoogleSheetsFirstTermFormControl.value,
          skuColumn: this.skuColumnGoogleSheetsFirstTermFormControl.value,
          urlColumn: this.urlColumnGoogleSheetsFirstTermFormControl.value,
          imageUrlColumn: this.imageUrlColumnGoogleSheetsFirstTermFormControl.value,
        },
        bigQueryConfig: {
          projectId: this.projectIdBigQueryFirstTermFormControl.value,
          dataset: this.datasetBigQueryFirstTermFormControl.value,
          table: this.tableBigQueryFirstTermFormControl.value,
          termColumn: this.termColumnBigQueryFirstTermFormControl.value,
          descriptionColumn: this.descriptionColumnBigQueryFirstTermFormControl.value,
          skuColumn: this.skuColumnBigQueryFirstTermFormControl.value,
          urlColumn: this.urlColumnBigQueryFirstTermFormControl.value,
          imageUrlColumn: this.imageUrlColumnBigQueryFirstTermFormControl.value,
          limit: this.limitBigQueryFirstTermFormControl.value,
        },
        listOfTermsConfig: {
          listOfTerms: this.listOfTermsFirstTermFormControl.value?.split(',')?.map(item => item.trim()).filter(item => item !== '') || [],
        }
      }
    };

    if (this.mustShowSecondTermConfig) {
      config['secondTermSourceConfig'] = {
        type: this.secondTermSourceSelected.replace(' second term', ''),
        googleSheetsConfig: {
          spreadsheetId: this.spreadsheetIdGoogleSheetsSecondTermFormControl.value,
          sheetName: this.sheetNameGoogleSheetsSecondTermFormControl.value,
          termColumn: this.termColumnGoogleSheetsSecondTermFormControl.value,
          startingRow: Number(this.startingRowGoogleSheetsSecondTermFormControl.value),
          descriptionColumn: this.descriptionColumnGoogleSheetsSecondTermFormControl.value,
          limit: Number(this.limitGoogleSheetsSecondTermFormControl.value),
        },
        bigQueryConfig: {
          projectId: this.projectIdBigQuerySecondTermFormControl.value,
          dataset: this.datasetBigQuerySecondTermFormControl.value,
          table: this.tableBigQuerySecondTermFormControl.value,
          termColumn: this.termColumnBigQuerySecondTermFormControl.value,
          descriptionColumn: this.descriptionColumnBigQuerySecondTermFormControl.value,
          limit: Number(this.limitBigQuerySecondTermFormControl.value),
        },
        googleTrendsConfig: {
          limit: Number(this.limitGoogleTrendsSecondTermFormControl.value) || 0,
        }
      }
    }

    this.dataSourcesConfigEvent.emit(config);

  }
}
