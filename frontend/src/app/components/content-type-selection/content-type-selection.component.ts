import { Component } from '@angular/core';
import { Output, EventEmitter } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-content-type-selection',
  standalone: true,
  imports: [MatButtonModule, MatIconModule, FormsModule, CommonModule],
  templateUrl: './content-type-selection.component.html',
  styleUrl: './content-type-selection.component.css',
})
export class ContentTypeSelectionComponent {
  title = 'Content Type Selection';
  inputTerm: string = ''; // Property to hold the user input
  @Output() contentTypeSelectionEvent = new EventEmitter<{ input: string; action: string }>();
  errorMessage: string = ''; // Property to hold error messages

  // Function to handle term logic
  private handleTerm(numberOfTerms: string, mustFindRelationship: boolean | null) {
    console.log(`Handling Term: numberOfTerms=${numberOfTerms}, mustFindRelationship=${mustFindRelationship}`);
    console.log('Input Term:', this.inputTerm);

    // Validate URL
    if (!this.isValidUrl(this.inputTerm)) {
      this.errorMessage = 'Please enter a valid URL.';
      return; // Exit if URL is invalid
    }

    // Prepare return object
    const returnObject: { [key: string]: string } = {
      URL: this.inputTerm,
      "number-of-terms": numberOfTerms,
    };
    if (mustFindRelationship !== null) {
      returnObject["must-find-relationship"] = mustFindRelationship.toString();
    }

    // Clear error message and emit event
    this.errorMessage = '';
    this.contentTypeSelectionEvent.emit({ input: JSON.stringify(returnObject), action: 'showDataSourcesConfig' });
    console.log('Emitted JSON:', JSON.stringify(returnObject));
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

  // Helper function to validate URL
  private isValidUrl(url: string): boolean {
    const urlPattern = new RegExp(
      '^(https?:\\/\\/)?' + // Protocol
      '((([a-zA-Z0-9\\-]+\\.)+[a-zA-Z]{2,})|' + // Domain name
      'localhost|' + // Localhost
      '\\d{1,3}(\\.\\d{1,3}){3})' + // OR IP (v4)
      '(\\:\\d+)?' + // Port
      '(\\/[-a-zA-Z0-9@:%._\\+~#=]*)*' + // Path
      '(\\?[;&a-zA-Z0-9@:%._\\+~#=]*)?' + // Query string
      '(\\#[-a-zA-Z0-9@:%._\\+~#=]*)?$', // Fragment locator
      'i'
    );
    return urlPattern.test(url);
  }
}