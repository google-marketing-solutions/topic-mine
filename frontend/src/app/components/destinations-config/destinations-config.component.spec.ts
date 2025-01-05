import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DestinationsConfigComponent } from './destinations-config.component';

describe('DestinationsConfigComponent', () => {
  let component: DestinationsConfigComponent;
  let fixture: ComponentFixture<DestinationsConfigComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DestinationsConfigComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DestinationsConfigComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
