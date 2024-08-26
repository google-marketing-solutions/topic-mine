import { Component, inject, signal, Output, EventEmitter } from '@angular/core';
import {
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { getPrompts } from '../../utils/prompts';
import { MatButtonModule } from '@angular/material/button';
import { MatAccordion, MatExpansionModule } from '@angular/material/expansion';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatRadioModule } from '@angular/material/radio';
import { MatDividerModule } from '@angular/material/divider';
import { MatSelectModule, MatSelectChange } from '@angular/material/select';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatListModule } from '@angular/material/list';
import { MatStepperModule } from '@angular/material/stepper';
import { MatCardModule } from '@angular/material/card';
import { GenerateAdsService } from '../../services/generate-ads.service';

@Component({
  selector: 'app-config-form',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    MatButtonModule,
    MatAccordion,
    MatExpansionModule,
    MatFormFieldModule,
    MatIconModule,
    MatInputModule,
    MatCheckboxModule,
    MatRadioModule,
    MatDividerModule,
    MatSelectModule,
    MatListModule,
    MatStepperModule,
    MatCardModule,
  ],
  templateUrl: './config-form.component.html',
  styleUrl: './config-form.component.css',
})
export class ConfigFormComponent {
  constructor(private generateAdsService: GenerateAdsService) {}
  private _snackBar = inject(MatSnackBar);
  readonly panelOpenState = signal(false);

  brands: string[] = [];
  @Output() selectBrandEvent = new EventEmitter<string>();
  products: string[] = [];
  trends: string[] = this.getTrends();
  prompts = getPrompts();
  prompt =
    this.prompts['EN']['GENERATION']['WITH_ASSOCIATIVE_TERM'][
      'WITHOUT_DESCRIPTIONS'
    ];

  configForm = new FormGroup({
    brandProducts: new FormControl('', [Validators.required]),
    gmc: new FormControl('gmcList', []),
    gmcId: new FormControl('', [Validators.required]),
    brands: new FormControl('select-brand', [Validators.required]),
    products: new FormControl([''], [Validators.required]),
    trendsSelection: new FormControl('externalTrends', [Validators.required]),
    externalTrends: new FormControl('', [Validators.required]),
    internalTrends: new FormControl('', [Validators.required]),
    numHeadlines: new FormControl('4', [Validators.required]),
    numDescriptions: new FormControl('4', [Validators.required]),
    language: new FormControl('EN', [Validators.required]),
    headlinesBlockList: new FormControl('', []),
    descriptionsBlockList: new FormControl('', []),
  });

  loadBrandsAndProducts() {
    this.brands = this.getBrands();
  }

  onBrandChange(change: MatSelectChange) {
    const brand = change.value as string;
    this.products = this.getProducts()[brand];
    this.selectBrandEvent.emit(brand);
  }

  onLanguageChange(change: MatSelectChange) {
    const language = change.value as string;
    this.prompt =
      this.prompts[language]['GENERATION']['WITH_ASSOCIATIVE_TERM'][
        'WITHOUT_DESCRIPTIONS'
      ];
  }

  getBrands() {
    const brands = ['One-Stop Shop', 'Fitness Glow', 'Skin Experts'];
    return brands;
  }

  getProducts() {
    const products: { [id: string]: any } = {
      'One-Stop Shop': [
        'SmartNest Thermostat',
        'VoiceBeam Smart Speaker',
        'ComfortContour Chair',
        'PosturePro Executive Chair',
        'HushZone ANC Headphones',
        'SerenitySounds Wireless Headphones',
        'PowerLite Ultrabook',
        'CreativePro Laptop',
      ],
      'Fitness Glow': [
        'ActivePulse Max',
        'FitLife Pro',
        'Trailblazer 2-Person Tent',
        'SunCatcher Portable Solar Charger',
        'TrekQueen Waterproof Hiking Boots',
        'TrailRunner Lightweight Hiking Shoes',
        'CampEasy Starter Kit',
        'SolarBright LED Camping Lantern',
      ],
      'Skin Experts': [
        'Purify & Protect Facial Cleanser',
        'GlowRenew Serum',
        'Sunscreen SPF 55',
        'Purify & protect facial cleanser',
      ],
    };
    return products;
  }

  getTrends() {
    const trends = [
      'Solar powered gadgets',
      'Best fitness tracker 2024',
      'Smart home',
      'skincare',
      'Ergonomic office chair',
      'Noise cancelling headphones',
      'Best laptop',
      'Camping gear for beginners',
      'Hiking boots for women',
    ];
    return trends;
  }

  generateAds() {
    const configFormData = {
      brand: this.configForm.get('brands')?.value,
      products: this.configForm.get('products')?.value,
      trendsSelection: this.configForm.get('trendsSelection')?.value,
      externalTrends: this.configForm.get('externalTrends')?.value,
      internalTrends: this.configForm.get('internalTrends')?.value,
      numHeadlines: this.configForm.get('numHeadlines')?.value,
      numDescriptions: this.configForm.get('numDescriptions')?.value,
      language: this.configForm.get('language')?.value,
      headlinesBlockList: this.configForm.get('headlinesBlockList')?.value,
      descriptionsBlockList: this.configForm.get('descriptionsBlockList')
        ?.value,
    };
    this.generateAdsService.generateAds(configFormData);
  }

  disableLoadGMCButton() {
    return !this.configForm.get('gmcId')?.valid;
  }

  openSnackBar(message: string) {
    this._snackBar.open(message, 'Close', {
      duration: 2000,
    });
  }
}
