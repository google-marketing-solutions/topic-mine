import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ContentGenerationSelectionConfigComponent } from './content-generation-selection-config.component';

describe('ContentGenerationSelectionConfigComponent', () => {
  let component: ContentGenerationSelectionConfigComponent;
  let fixture: ComponentFixture<ContentGenerationSelectionConfigComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ContentGenerationSelectionConfigComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ContentGenerationSelectionConfigComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
