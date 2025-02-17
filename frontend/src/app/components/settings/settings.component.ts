import { Component } from '@angular/core';
import { FormControl, FormGroupDirective, NgForm, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { ErrorStateMatcher } from '@angular/material/core';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';
import { GlobalService } from '../../services/global.service';
import { Router } from '@angular/router';

/** Error when invalid control is dirty, touched, or submitted. */
export class MyErrorStateMatcher implements ErrorStateMatcher {
  isErrorState(control: FormControl | null, form: FormGroupDirective | NgForm | null): boolean {
    const isSubmitted = form && form.submitted;
    return !!(control && control.invalid && (control.dirty || control.touched || isSubmitted));
  }
}

@Component({
  selector: 'app-settings',
  imports: [FormsModule, ReactiveFormsModule, MatInputModule, MatFormFieldModule, MatButtonModule],
  templateUrl: './settings.component.html',
  styleUrl: './settings.component.css'
})
export class SettingsComponent {
  constructor(public globalService: GlobalService, private router: Router) {}


  matcher = new MyErrorStateMatcher();

  isSaveButtonDisabled: boolean = true;
  isSendingRequest: boolean = false;
  mustOpenModal: boolean = false;
  requestFailed: boolean = false;

  baseUrlFormControl = new FormControl('', [Validators.required, Validators.nullValidator]);
  customerIdFormControl = new FormControl('', []);
  developerTokenFormControl = new FormControl('', []);

  ngOnInit() {
    this.baseUrlFormControl.valueChanges.subscribe(() => this.updateSaveButtonState());
    this.customerIdFormControl.valueChanges.subscribe(() => this.updateSaveButtonState());
    this.developerTokenFormControl.valueChanges.subscribe(() => this.updateSaveButtonState());
  }

  updateSaveButtonState() {
    if (this.baseUrlFormControl.valid) {
      this.isSaveButtonDisabled = false;
    } else {
      this.isSaveButtonDisabled = true;
    }

    if (this.customerIdFormControl.value === '' || this.developerTokenFormControl.value === '') {
      this.mustOpenModal = true;
    } else {
      this.mustOpenModal = false;
    }
  }

  goBack() {
    this.router.navigateByUrl('/home');
  }

  openModal () {

  }

  saveSettings() {
    this.globalService.setBaseUrl(this.baseUrlFormControl.value!);
    this.globalService.setCustomerId(this.customerIdFormControl.value!);
    this.globalService.setDeveloperToken(this.developerTokenFormControl.value!);
  }

}
