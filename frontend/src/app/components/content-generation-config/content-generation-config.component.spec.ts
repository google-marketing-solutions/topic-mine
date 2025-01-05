import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ContentGenerationConfigComponent } from './content-generation-config.component';

describe('ContentGenerationConfigComponent', () => {
  let component: ContentGenerationConfigComponent;
  let fixture: ComponentFixture<ContentGenerationConfigComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ContentGenerationConfigComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ContentGenerationConfigComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
