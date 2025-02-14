import { Component, Input, signal, OnInit } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatAccordion, MatExpansionModule } from '@angular/material/expansion';
import { MatIconModule } from '@angular/material/icon';
import { MatDividerModule } from '@angular/material/divider';
import { MatCardModule } from '@angular/material/card';
import { getAssociations } from '../../utils/associations';
import { getEntries } from '../../utils/entries';
import { Association } from '../../models/association';
import { Entry } from '../../models/entry';
import { GenerateAdsService } from '../../services/generate-ads.service';
import { CommonModule } from '@angular/common';
import {MatTableModule} from '@angular/material/table';

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
    MatTableModule,
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
  entries: Entry[] = [];
  readonly panelOpenState = signal(false);
  expand: boolean = true;
  displayedColumns: string[] = ['Product', 'Trend', 'Headlines', 'Descriptions'];


  constructor(private generateAdsService: GenerateAdsService) {
    generateAdsService.generateAds$.subscribe((configFormData: any) => {
      this.updateEntries(configFormData);
    });
  }

  ngAfterViewInit() {
    this.updateEntries({});
  }

  updateEntries(configFormData: any) {
    const entriesAll = getEntries();
    this.entries = entriesAll;

    try {
      const selectedProducts = configFormData['products'].map((p: string) => p.toLowerCase());
      const selectedTrends = configFormData['trends'].map((p: string) => p.toLowerCase());
      const numHeadlines = configFormData['numHeadlines'];
      const numDescriptions = configFormData['numDescriptions'];

      if (numHeadlines === 0 || numDescriptions === 0 || selectedProducts.length === 0 || selectedTrends.length === 0) {
        this.entries = []
        return;
      }

      this.entries = entriesAll.filter(entry =>{
        const lowerCaseTerm = entry.Term.toLowerCase();
        const lowerCaseTrend = entry.Trend.toLowerCase();

        console.log('ENTRY TERM: ' + lowerCaseTerm)
        console.log('ENTRY TREND: ' + lowerCaseTrend)

        const ok =  selectedProducts.some((product: string) => lowerCaseTerm.includes(product.toLowerCase())) && selectedTrends.some((trend: string) => lowerCaseTrend.includes(trend.toLowerCase()));

        if (ok) {
          console.log('SIIIII');
        } else {
          console.log('NOOOOO');
        }

        return ok;
      }).map(product => {
        return {
          ...product,
          Headlines: product.Headlines.slice(0, numHeadlines),
          Descriptions: product.Descriptions.slice(0, numDescriptions)
        };
      });
    } catch (error) {
      this.entries = []
    }


    console.log('LEN ENTRIES: ' + this.entries.length)
  }

  hasRelationship(entry: Entry): boolean {
    return entry.Relationship === "TRUE"
  }

  shouldHideContent(): boolean {
    return this.entries.length === 0;
  }

  onFormSubmit(event: any) {
    this.entries = event;
  }

  exportToSA360Template() {}

  exportToDV360Template() {}
}
