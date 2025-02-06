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

import { Component, Output, EventEmitter, ViewChild, Input } from '@angular/core';
import {
  FormControl,
  FormGroupDirective,
  NgForm,
  Validators,
  FormsModule,
  ReactiveFormsModule,
} from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatDividerModule } from '@angular/material/divider';
import { ErrorStateMatcher } from '@angular/material/core';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatChipsModule, MatChipListbox } from '@angular/material/chips';



/** Error when invalid control is dirty, touched, or submitted. */
export class MyErrorStateMatcher implements ErrorStateMatcher {
  isErrorState(control: FormControl | null, form: FormGroupDirective | NgForm | null): boolean {
    const isSubmitted = form && form.submitted;
    return !!(control && control.invalid && (control.dirty || control.touched || isSubmitted));
  }
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


export interface ContentGenerationConfig {
  generateKeywords: boolean;
  generatePaths: boolean;
  enableFeatureExtraction: boolean;
  enableURLValidation: boolean;
  numberOfHeadlines: number;
  numberOfDescriptions: number;
  headlinesBlocklist: string[] | null;
  descriptionsBlocklist: string[] | null;
  headlinesRegexBlocklist: string[] | null;
  descriptionsRegexBlocklist: string[] | null;
  genericHeadlines: string[] | null;
  genericDescriptions: string[] | null;
  advertiserName: string;
  country: string;
  geminiModel: string;
  language: string;
}

@Component({
  selector: 'app-content-generation-config',
  standalone: true,
  imports: [MatChipListbox, MatChipsModule, FormsModule, ReactiveFormsModule, MatButtonModule, MatCheckboxModule, MatDividerModule, MatFormFieldModule, MatGridListModule, MatIconModule, MatInputModule, MatTooltipModule],
  templateUrl: './content-generation-config.component.html',
  styleUrl: './content-generation-config.component.css',
})
export class ContentGenerationConfigComponent {
  // CHIPS FOR BASIC OPTIONS
  options: string[] = ['Generate keywords', 'Generate paths', 'Enable feature extraction', 'Enable URL validation'];
  @ViewChild(MatChipListbox) chipList!: MatChipListbox;
  ngAfterViewInit() {
    this.getSelectedChips();

   this.chipList.chipSelectionChanges.subscribe(changes => {
     this.getSelectedChips();
   });
 }
  getSelectedChips() {
    const selected = this.chipList.selected;
    if (selected) {
      if (Array.isArray(selected)) {
        this.mySelectedOptions = selected.map(chip => chip.value);
      } else {
        this.mySelectedOptions = [selected.value];
      }
    } else {
      this.mySelectedOptions = [];
    }
  }
  mySelectedOptions: string[] = [];



  // FOR HANDLING BUTTON STATUS
  @Input() isSendingRequest: boolean = false;
  @Input() requestFailed: boolean = false;

  @Output() contentGenerationConfigEvent = new EventEmitter<ContentGenerationConfig>();
  @Output() changeViewEvent = new EventEmitter<string>();
  @Output() nextButtonDisabledEvent = new EventEmitter<boolean>();

  headlinesCounterFormControl = new FormControl('', [Validators.required, Validators.min(1), Validators.max(15), integerValidator()]);
  descriptionsCounterFormControl = new FormControl('', [Validators.required, Validators.min(1), Validators.max(4), integerValidator()]);
  advertiserNameFormControl = new FormControl('', [Validators.required, Validators.nullValidator]);
  countryFormControl = new FormControl('', [Validators.required, Validators.nullValidator]);
  geminiModelFormControl = new FormControl('', []);
  headlinesBlocklistingFormControl = new FormControl('', []);
  descriptionsBlocklistingFormControl = new FormControl('', []);
  headlinesRegexBlocklistingFormControl = new FormControl('', []);
  descriptionsRegexBlocklistingFormControl = new FormControl('', []);
  genericHeadlinesFormControl = new FormControl('', []);
  genericDescriptionsFormControl = new FormControl('', []);


  matcher = new MyErrorStateMatcher();

  isStartButtonDisabled: boolean = true;


  selectedLanguage: string = 'Spanish';

  selectLanguage(l: string) {
    this.selectedLanguage = l;
    this.updateStartButtonState();
  }

  ngOnInit() {
    this.headlinesCounterFormControl.valueChanges.subscribe(() => this.updateStartButtonState());
    this.descriptionsCounterFormControl.valueChanges.subscribe(() => this.updateStartButtonState());
    this.advertiserNameFormControl.valueChanges.subscribe(() => this.updateStartButtonState());
    this.countryFormControl.valueChanges.subscribe(() => this.updateStartButtonState());
  }

  updateStartButtonState() {
    this.isStartButtonDisabled = !(
      this.headlinesCounterFormControl.valid &&
      this.descriptionsCounterFormControl.valid &&
      this.advertiserNameFormControl.valid &&
      this.countryFormControl.valid
    );
    this.nextButtonDisabledEvent.emit(this.isStartButtonDisabled);
  }

  goBack() {
    this.changeViewEvent.emit('destinations-config');
  }

  sendContentGenerationConfig() {
    const config: ContentGenerationConfig = {
      generateKeywords: this.mySelectedOptions.includes('Generate keywords'),
      generatePaths: this.mySelectedOptions.includes('Generate paths'),
      enableFeatureExtraction: this.mySelectedOptions.includes('Enable feature extraction'),
      enableURLValidation: this.mySelectedOptions.includes('Enable URL validation'),
      numberOfHeadlines: Number(this.headlinesCounterFormControl.value) || 0,
      numberOfDescriptions: Number(this.descriptionsCounterFormControl.value) || 0,
      headlinesBlocklist: this.headlinesBlocklistingFormControl.value?.split(',')?.map(item => item.trim()).filter(item => item !== '') || null,
      descriptionsBlocklist: this.descriptionsBlocklistingFormControl.value?.split(',')?.map(item => item.trim()).filter(item => item !== '') || null,
      headlinesRegexBlocklist: this.headlinesRegexBlocklistingFormControl.value?.split(',')?.map(item => item.trim()).filter(item => item !== '') || null,
      descriptionsRegexBlocklist: this.descriptionsRegexBlocklistingFormControl.value?.split(',')?.map(item => item.trim()).filter(item => item !== '') || null,
      genericHeadlines: this.genericHeadlinesFormControl.value?.split(',')?.map(item => item.trim()).filter(item => item !== '') || null,
      genericDescriptions: this.genericDescriptionsFormControl.value?.split(',')?.map(item => item.trim()).filter(item => item !== '') || null,
      advertiserName: this.advertiserNameFormControl.value!,
      country: this.countryFormControl.value!,
      geminiModel: this.geminiModelFormControl.value ?? 'gemini-1.5-flash',
      language: this.selectedLanguage,
    };

    this.contentGenerationConfigEvent.emit(config);
  }
}
