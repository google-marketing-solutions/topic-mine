import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NavbarComponent } from './modules/navbar/navbar.component';
import { ConfigFormComponent } from './modules/config-form/config-form.component';
import { ResultsComponent } from './modules/results/results.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet,
    NavbarComponent,
    ConfigFormComponent,
    ResultsComponent,
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent {
  title = 'topic-mine';
  selectedBrand: string = '';

  selectBrand(brand: string) {
    this.selectedBrand = brand;
  }
}
