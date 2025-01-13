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
import { Output, EventEmitter } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-content-type-selection',
  imports: [MatButtonModule, MatIconModule],
  templateUrl: './content-type-selection.component.html',
  styleUrl: './content-type-selection.component.css',
})
export class ContentTypeSelectionComponent {
  title = 'Content Type Selection';
  @Output() contentTypeSelectionEvent = new EventEmitter<string>();

  sendContentTypeSelection() {
    // TODO: implement logic to gather params here.
    this.contentTypeSelectionEvent.emit(`${this.title} sent to parent!`);
  }
}
