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

import {
  FormControl,
  FormGroupDirective,
  NgForm,
  Validators,
  FormsModule,
  ReactiveFormsModule,
} from '@angular/forms';
import { ErrorStateMatcher } from '@angular/material/core';
import { Component } from '@angular/core';
import { Output, EventEmitter } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatDividerModule } from '@angular/material/divider';
import { MatIconModule } from '@angular/material/icon';
import { MatSelectModule } from '@angular/material/select';
import { MatInputModule } from '@angular/material/input';

/** Error when invalid control is dirty, touched, or submitted. */
export class MyErrorStateMatcher implements ErrorStateMatcher {
  isErrorState(control: FormControl | null, form: FormGroupDirective | NgForm | null): boolean {
    const isSubmitted = form && form.submitted;
    return !!(control && control.invalid && (control.dirty || control.touched || isSubmitted));
  }
}

interface OutputConfig {
  outputFormat: string;
  spreadsheetId: string;
  sheetName: string;
}

@Component({
  selector: 'app-destinations-config',
  standalone: true,
  imports: [FormsModule, ReactiveFormsModule, MatButtonModule, MatDividerModule, MatIconModule, MatInputModule, MatSelectModule],
  templateUrl: './destinations-config.component.html',
  styleUrl: './destinations-config.component.css',
})
export class DestinationsConfigComponent {
  title = 'Destinations Configuration';
  @Output() destinationsConfigEvent = new EventEmitter<OutputConfig>();

  outputFormats: string[] = ['Google Ads', 'SA360', 'DV360'];

  isNextButtonDisabled: boolean = true;

  outputFormatFormControl = new FormControl('', [Validators.required, Validators.nullValidator]);
  spreadsheetIdFormControl = new FormControl('', [Validators.required, Validators.nullValidator]);
  sheetNameFormControl = new FormControl('', [Validators.required, Validators.nullValidator]);

  matcher = new MyErrorStateMatcher();

  ngOnInit() {
    this.outputFormatFormControl.valueChanges.subscribe(() => this.updateNextButtonState());
    this.spreadsheetIdFormControl.valueChanges.subscribe(() => this.updateNextButtonState());
    this.sheetNameFormControl.valueChanges.subscribe(() => this.updateNextButtonState());
  }

  updateNextButtonState() {
    if (this.outputFormatFormControl.valid &&
        this.spreadsheetIdFormControl.valid &&
        this.sheetNameFormControl.valid) {
          this.isNextButtonDisabled = false;
          return;
        }

    this.isNextButtonDisabled = true;
  }

  goBack() {

  }

  sendOutputConfig() {
    const config: OutputConfig = {
      outputFormat: this.outputFormatFormControl.value!,
      spreadsheetId: this.spreadsheetIdFormControl.value!,
      sheetName: this.sheetNameFormControl.value!,
    }

    this.destinationsConfigEvent.emit(config);
  }
}
