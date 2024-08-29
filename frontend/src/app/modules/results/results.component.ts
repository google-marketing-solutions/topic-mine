import { Component, Input, signal, OnInit } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatAccordion, MatExpansionModule } from '@angular/material/expansion';
import { MatIconModule } from '@angular/material/icon';
import { MatDividerModule } from '@angular/material/divider';
import { MatCardModule } from '@angular/material/card';
import { getAssociations } from '../../utils/associations';
import { Association } from '../../models/association';
import { GenerateAdsService } from '../../services/generate-ads.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-results',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatAccordion,
    MatExpansionModule,
    MatIconModule,
    MatDividerModule,
    MatCardModule,
  ],
  templateUrl: './results.component.html',
  styleUrl: './results.component.css',
  styles: [`
    .association-card {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    h3 {
      margin: 0;
      font-size: 1.5em;
    }
    .product-trend-info {
      display: flex;
      gap: 1rem;
      .product, .trend {
        font-size: 0.9em;
        color: gray;
      }
    }
  }

  .card-content {
    .headlines-section, .descriptions-section {
      margin: 1rem 0;
      h4 {
        display: flex;
        align-items: center;
        font-size: 1.2em;
        mat-icon {
          margin-right: 0.5rem;
        }
      }
      .headlines-container, .descriptions-container {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
      }
      .headline-item, .description-item {
        flex: 1 1 45%; /* Adjusts items to be side by side */
        font-size: 1em;
      }
    }
  }

  mat-card-actions {
    margin-top: 1rem;
  }
}
  `]
})
export class ResultsComponent {
  @Input() selectedBrand: string = '';
  @Input() entries: Object[] = [];
  associations: Association[] = [];
  readonly panelOpenState = signal(false);
  expand: boolean = true;

  constructor(private generateAdsService: GenerateAdsService) {
    generateAdsService.generateAds$.subscribe((configFormData: any) => {
      console.log(configFormData);
      this.updateAssociations(configFormData);
    });
  }

  ngAfterViewInit() {
    console.log('AfterViewInit');
    console.log(this.selectedBrand);
    this.updateAssociations({});
  }

  updateAssociations(configFormData: any) {
    const associationsAll = getAssociations()[this.selectedBrand];
    this.associations = associationsAll;
  }

  onFormSubmit(event: any) {
    this.entries = event;
    console.log('entries on results component: ' + this.entries)
  }

  exportToSA360Template() {}

  exportToDV360Template() {}
}
