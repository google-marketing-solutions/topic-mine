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

import { Component, Output, EventEmitter } from '@angular/core';
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


interface ContentGenerationConfig {
  generateKeywords: boolean;
  generatePaths: boolean;
  enableFeatureExtraction: boolean;
  enableURLValidation: boolean;
  numberOfHeadlines: number;
  numberOfDescriptions: number;
  headlinesBlocklisting: string[] | null;
  descriptionsBlocklisting: string[] | null;
  genericHeadlines: string[] | null;
  genericDescriptions: string[] | null;
}

@Component({
  selector: 'app-content-generation-config',
  standalone: true,
  imports: [FormsModule, ReactiveFormsModule, MatButtonModule, MatCheckboxModule, MatDividerModule, MatFormFieldModule, MatGridListModule, MatIconModule, MatInputModule, MatTooltipModule],
  templateUrl: './content-generation-config.component.html',
  styleUrl: './content-generation-config.component.css',
})
export class ContentGenerationConfigComponent {
  title = 'Data Sources Configuration';
  @Output() contentGenerationConfigEvent = new EventEmitter<ContentGenerationConfig>();

  headlinesCounterFormControl = new FormControl('', [Validators.required, Validators.min(1), Validators.max(15), integerValidator()]);
  descriptionsCounterFormControl = new FormControl('', [Validators.required, Validators.min(1), Validators.max(4), integerValidator()]);
  headlinesBlocklistingFormControl = new FormControl('', []);
  descriptionsBlocklistingFormControl = new FormControl('', []);
  genericHeadlinesFormControl = new FormControl('', []);
  genericDescriptionsFormControl = new FormControl('', []);



  matcher = new MyErrorStateMatcher();

  generateKeywords = false;
  generatePaths = false;
  enableFeatureExtraction = false;
  enableURLValidation = false;


  isStartButtonDisabled: boolean = true;
  ngOnInit() {
    this.headlinesCounterFormControl.valueChanges.subscribe(() => this.updateStartButtonState());
    this.descriptionsCounterFormControl.valueChanges.subscribe(() => this.updateStartButtonState());
  }
  updateStartButtonState() {
    this.isStartButtonDisabled = !(this.headlinesCounterFormControl.valid && this.descriptionsCounterFormControl.valid);
  }




  sendContentGenerationConfig() {
    const config: ContentGenerationConfig = {
      generateKeywords: this.generateKeywords,
      generatePaths: this.generatePaths,
      enableFeatureExtraction: this.enableFeatureExtraction,
      enableURLValidation: this.enableURLValidation,
      numberOfHeadlines: Number(this.headlinesCounterFormControl.value) || 0,
      numberOfDescriptions: Number(this.descriptionsCounterFormControl.value) || 0,
      headlinesBlocklisting: this.headlinesBlocklistingFormControl.value?.split(',')?.map(item => item.trim()).filter(item => item !== '') || null,
      descriptionsBlocklisting: this.descriptionsBlocklistingFormControl.value?.split(',')?.map(item => item.trim()).filter(item => item !== '') || null,
      genericHeadlines: this.genericHeadlinesFormControl.value?.split(',')?.map(item => item.trim()).filter(item => item !== '') || null,
      genericDescriptions: this.genericDescriptionsFormControl.value?.split(',')?.map(item => item.trim()).filter(item => item !== '') || null,
    };

    this.contentGenerationConfigEvent.emit(config);
  }
}
