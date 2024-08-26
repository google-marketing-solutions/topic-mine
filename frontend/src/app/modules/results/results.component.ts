import { Component, Input, signal } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatAccordion, MatExpansionModule } from '@angular/material/expansion';
import { MatIconModule } from '@angular/material/icon';
import { MatDividerModule } from '@angular/material/divider';
import { MatCardModule } from '@angular/material/card';
import { getAssociations } from '../../utils/associations';
import { Association } from '../../models/association';
import { GenerateAdsService } from '../../services/generate-ads.service';

@Component({
  selector: 'app-results',
  standalone: true,
  imports: [
    MatButtonModule,
    MatAccordion,
    MatExpansionModule,
    MatIconModule,
    MatDividerModule,
    MatCardModule,
  ],
  templateUrl: './results.component.html',
  styleUrl: './results.component.css',
})
export class ResultsComponent {
  @Input() selectedBrand: string = '';
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

  exportToSA360Template() {}

  exportToDV360Template() {}
}
