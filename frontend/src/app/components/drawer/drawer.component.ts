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

import { Component } from '@angular/core';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatStepperModule } from '@angular/material/stepper';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { ContentTypeSelectionComponent } from '../content-type-selection/content-type-selection.component';
import { DataSourcesConfigComponent } from '../data-sources-config/data-sources-config.component';
import { DestinationsConfigComponent } from '../destinations-config/destinations-config.component';
import { ContentGenerationConfigComponent } from '../content-generation-config/content-generation-config.component';

@Component({
  selector: 'app-drawer',
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
  showCTS = true;
  showSC = false;
  showDC = false;
  showCGC = false;

  receiveContentTypeSelection(value: string) {
    console.log(value);
  }

  receiveDataSourcesConfig(value: string) {
    console.log(value);
  }

  receiveDestinationsConfig(value: string) {
    console.log(value);
  }

  receiveContentGenerationConfig(value: string) {
    console.log(value);
  }

  showContentGenerationSelectionConfig() {
    this.showCTS = true;
    this.showSC = false;
    this.showDC = false;
    this.showCGC = false;
  }

  showDataSourcesConfig() {
    this.showSC = true;
    this.showCTS = false;
    this.showDC = false;
    this.showCGC = false;
  }

  showDestinationsConfig() {
    this.showDC = true;
    this.showSC = false;
    this.showCTS = false;
    this.showCGC = false;
  }

  showContentGenerationConfig() {
    this.showCGC = true;
    this.showDC = false;
    this.showSC = false;
    this.showCTS = false;
  }
}
