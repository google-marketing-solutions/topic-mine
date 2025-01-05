import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatIconModule } from '@angular/material/icon';
import { NavbarComponent } from './components/navbar/navbar.component';
import { ContentGenerationSelectionConfigComponent } from './components/content-generation-selection-config/content-generation-selection-config.component';
import { DataSourcesConfigComponent } from './components/data-sources-config/data-sources-config.component';
import { DestinationsConfigComponent } from './components/destinations-config/destinations-config.component';
import { ContentGenerationConfigComponent } from './components/content-generation-config/content-generation-config.component';

@Component({
  selector: 'app-root',
  imports: [
    RouterOutlet,
    MatButtonModule,
    MatSidenavModule,
    MatIconModule,
    NavbarComponent,
    ContentGenerationSelectionConfigComponent,
    DataSourcesConfigComponent,
    DestinationsConfigComponent,
    ContentGenerationConfigComponent,
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent {
  title = 'frontend';
  showFiller = false;

  showContentGenerationSelectionConfig() {}

  showDataSourcesConfig() {}

  showDestinationsConfig() {}

  showContentGenerationConfig() {}
}
