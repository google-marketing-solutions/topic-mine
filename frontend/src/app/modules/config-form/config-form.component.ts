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
import { HttpClient } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';
import { isVariableStatement } from 'typescript';

@Component({
  selector: 'app-config-form',
  standalone: true,
  imports: [
    HttpClientModule,
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
  private _snackBar = inject(MatSnackBar);
  readonly panelOpenState = signal(false);

  brands: string[] = [];
  @Output() selectBrandEvent = new EventEmitter<string>();
  @Output() formSubmit = new EventEmitter<any>();
  products: string[] = [];
  trends: string[] = this.getTrends();

  promptHeadlines: string = '';
  promptDescriptions: string = '';

  configForm = new FormGroup({
    brandsProductsSelection: new FormControl('gmcList', []),
    gmcId: new FormControl('', [Validators.required]),
    brands: new FormControl('select-brand', [Validators.required]),
    products: new FormControl([''], [Validators.required]),
    customerProvidedBrand: new FormControl('', [Validators.required]),
    customerProvidedProducts: new FormControl('', [Validators.required]),
    trendsSelection: new FormControl('externalTrends', [Validators.required]),
    externalTrends: new FormControl([''], [Validators.required]),
    internalTrends: new FormControl('', [Validators.required]),
    numHeadlines: new FormControl('4', [Validators.required]),
    numDescriptions: new FormControl('4', [Validators.required]),
    language: new FormControl('EN', [Validators.required]),
    headlinesBlockList: new FormControl('', []),
    descriptionsBlockList: new FormControl('', []),
  });

  constructor(private generateAdsService: GenerateAdsService, private http: HttpClient) {
    this.configForm.valueChanges.subscribe((data) => {
      this.replacePromptParams();
    });
  }

  replacePromptParams() {
    const language = this.configForm.get('language')?.value!;
    const prompts = getPrompts();
    // Headlines
    if (this.configForm.get('headlinesBlockList')?.value) {
      this.promptHeadlines =
        prompts[language]['GENERATION']['WITH_ASSOCIATIVE_TERM'][
          'WITHOUT_DESCRIPTIONS'
        ]['HEADLINES']['WITH_BLOCK_LIST'];
    } else {
      this.promptHeadlines =
        prompts[language]['GENERATION']['WITH_ASSOCIATIVE_TERM'][
          'WITHOUT_DESCRIPTIONS'
        ]['HEADLINES']['WITHOUT_BLOCK_LIST'];
    }
    // Descriptions
    if (this.configForm.get('descriptionsBlockList')?.value!) {
      this.promptDescriptions =
        prompts[language]['GENERATION']['WITH_ASSOCIATIVE_TERM'][
          'WITHOUT_DESCRIPTIONS'
        ]['DESCRIPTIONS']['WITH_BLOCK_LIST'];
    } else {
      this.promptDescriptions =
        prompts[language]['GENERATION']['WITH_ASSOCIATIVE_TERM'][
          'WITHOUT_DESCRIPTIONS'
        ]['DESCRIPTIONS']['WITHOUT_BLOCK_LIST'];
    }
    // Products selection
    const products = this.getProductsFromForm();
    const product = products[Math.floor(Math.random() * products.length)];
    // Trends selection
    const trends = this.getTrendsFromForm();
    const trend = trends[Math.floor(Math.random() * trends.length)];

    const headlinesBlockList = this.configForm
      .get('headlinesBlockList')
      ?.value!.split('\n')
      .join(', ') as string;
    const descriptionsBlockList = this.configForm
      .get('descriptionsBlockList')
      ?.value!.split('\n')
      .join(', ') as string;

    this.promptHeadlines = this.promptHeadlines
      .replaceAll('{n}', this.configForm.get('numHeadlines')?.value!)
      .replaceAll('{term}', product)
      .replaceAll('{associative_term}', trend)
      .replaceAll('{association_reason}', trend)
      .replaceAll('{company}', this.configForm.get('brands')?.value!)
      .replaceAll('{headlines_block_list}', headlinesBlockList);
    this.promptDescriptions = this.promptDescriptions
      .replaceAll('{n}', this.configForm.get('numHeadlines')?.value!)
      .replaceAll('{term}', product)
      .replaceAll('{associative_term}', trend)
      .replaceAll('{association_reason}', trend)
      .replaceAll('{company}', this.configForm.get('brands')?.value!)
      .replaceAll('{descriptions_block_list}', descriptionsBlockList);
  }

  getBrandFromForm() {
    let brand: string;
    if (this.configForm.get('brandsProductsSelection')?.value === 'gmcList') {
      brand = this.configForm.get('brands')?.value!;
    } else {
      brand = this.configForm.get('customerProvidedBrand')?.value!;
    }
    return brand;
  }

  getProductsFromForm() {
    let products: string[] = [];
    if (this.configForm.get('brandsProductsSelection')?.value === 'gmcList') {
      products = this.configForm.get('products')?.value!;
    } else {
      products = this.configForm
        .get('customerProvidedProducts')
        ?.value!.split('\n')!;
    }
    return products;
  }

  getTrendsFromForm() {
    let trends: string[] = [];
    if (this.configForm.get('trendsSelection')?.value === 'externalTrends') {
      trends = this.configForm.get('externalTrends')?.value!;
    } else {
      trends = this.configForm.get('internalTrends')?.value!.split('\n')!;
    }
    return trends;
  }

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
    this.replacePromptParams();
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
      brandsProductsSelection: this.configForm.get('brandsProductsSelection')?.value,
      brand: this.getBrandFromForm(),
      products: this.getProductsFromForm(),
      trendsSelection: this.configForm.get('trendsSelection')?.value,
      trends: this.getTrendsFromForm(),
      numHeadlines: this.configForm.get('numHeadlines')?.value,
      numDescriptions: this.configForm.get('numDescriptions')?.value,
      language: this.configForm.get('language')?.value,
      headlinesBlockList: this.configForm.get('headlinesBlockList')?.value,
      descriptionsBlockList: this.configForm.get('descriptionsBlockList')?.value,
    };
    this.generateAdsService.generateAds(configFormData);
}

  disableLoadGMCButton() {
    return !this.configForm.get('gmcId')?.valid;
  }

  enableStep1NextButton() {
    const products = this.getProductsFromForm();
    let valid: boolean = false; // check this
    if (this.configForm.get('brandsProductsSelection')?.value === 'gmcList') {
      valid = (this.configForm.get('gmcId')?.valid &&
        this.configForm.get('brands')?.valid &&
        this.configForm.get('brands')?.value !== 'select-brand' &&
        products &&
        products.length > 0 &&
        products[0] !== '')!;
    } else {
      valid = (this.configForm.get('customerProvidedBrand')?.valid &&
        products &&
        products.length > 0 &&
        products[0] !== '')!;
    }
    return valid;
  }

  enableStep2NextButton() {
    const externalTrends = this.configForm.get('externalTrends')
      ?.value as string[];
    // Users can select either external or internal trends
    const valid =
      (externalTrends && externalTrends.length > 0 && externalTrends[0]) ||
      this.configForm.get('internalTrends')?.valid;
    return valid;
  }

  enableStep3Button() {
    const valid =
      this.configForm.get('numHeadlines')?.valid &&
      this.configForm.get('numDescriptions')?.valid &&
      this.configForm.get('language')?.valid;
    return valid;
  }

  openSnackBar(message: string) {
    this._snackBar.open(message, 'Close', {
      duration: 2000,
    });
  }
}
