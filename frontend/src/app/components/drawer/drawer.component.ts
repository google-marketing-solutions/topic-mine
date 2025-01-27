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


import { MatSidenavModule } from '@angular/material/sidenav';
import { MatStepperModule } from '@angular/material/stepper';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { ContentTypeSelectionComponent } from '../content-type-selection/content-type-selection.component';
import { DataSourcesConfigComponent } from '../data-sources-config/data-sources-config.component';
import { DestinationsConfigComponent } from '../destinations-config/destinations-config.component';
import { ContentGenerationConfigComponent } from '../content-generation-config/content-generation-config.component';

import { Component, ViewChild } from '@angular/core';
import { MatStepper } from '@angular/material/stepper';


@Component({
  selector: 'app-drawer',
  standalone: true,
  imports: [
    MatSidenavModule,
    MatStepperModule,
    MatButtonModule,
    MatIconModule,
    ContentTypeSelectionComponent,
    DataSourcesConfigComponent,
    DestinationsConfigComponent,
    ContentGenerationConfigComponent,
  ],
  templateUrl: './drawer.component.html',
  styleUrl: './drawer.component.css',
})
export class DrawerComponent {
  @ViewChild(MatStepper) stepper!: MatStepper;

  showCTS = true;
  showSC = false;
  showDC = false;
  showCGC = false;

  receiveContentTypeSelection(event: { input: string; action: string }) {
    console.log('Received Event:', event);

    if (event.action === 'showDataSourcesConfig') {
      console.log('Input Term:', event.input); // Process the input term
      this.showDataSourcesConfig();
    }
  }


  receiveDataSourcesConfig(value: any) {
    console.log(value);
  }

  receiveDestinationsConfig(value: any) {
    console.log(value);

  }

  receiveContentGenerationConfig(value: any) {
    console.log(`Content Generation Config Event: ${value}`);
  }

  showContentGenerationSelectionConfig() {
    this.showCTS = true;
    this.showSC = false;
    this.showDC = false;
    this.showCGC = false;
    this.stepper.previous();
  }

  showDataSourcesConfig() {
    this.showSC = true;
    this.showCTS = false;
    this.showDC = false;
    this.showCGC = false;
    this.stepper.next();
  }

  showDestinationsConfig() {
    this.showDC = true;
    this.showSC = false;
    this.showCTS = false;
    this.showCGC = false;
    this.stepper.next();
  }

  showContentGenerationConfig() {
    this.showCGC = true;
    this.showDC = false;
    this.showSC = false;
    this.showCTS = false;
    this.stepper.next();
  }
}
