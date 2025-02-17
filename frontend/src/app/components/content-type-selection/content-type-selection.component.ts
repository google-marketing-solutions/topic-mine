import { Component } from '@angular/core';
import { Output, EventEmitter } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

export interface ContentTypeConfig {
  numberOfTerms: number;
  mustFindRelationship: boolean | null;
}

@Component({
  selector: 'app-content-type-selection',
  standalone: true,
  imports: [MatButtonModule, MatIconModule, FormsModule, CommonModule],
  templateUrl: './content-type-selection.component.html',
  styleUrl: './content-type-selection.component.css',
})
export class ContentTypeSelectionComponent {
  @Output() contentTypeSelectionEvent = new EventEmitter<ContentTypeConfig>();
  errorMessage: string = '';

  private handleTerm(numberOfTerms: string, mustFindRelationship: boolean | null) {

    const returnObject: ContentTypeConfig = {
      numberOfTerms: parseInt(numberOfTerms),
      mustFindRelationship: mustFindRelationship,
    };

    this.errorMessage = '';
    this.contentTypeSelectionEvent.emit(returnObject);
  }

  oneInputTerm() {
    this.handleTerm("1", null); // No relationship for one input term
  }

  twoInputTermFindRelationship() {
    this.handleTerm("2", false); // Must find relationship is false
  }

  twoInputTermForceRelationship() {
    this.handleTerm("2", true); // Must find relationship is true
  }
}