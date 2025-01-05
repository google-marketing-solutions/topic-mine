import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DataSourcesConfigComponent } from './data-sources-config.component';

describe('DataSourcesConfigComponent', () => {
  let component: DataSourcesConfigComponent;
  let fixture: ComponentFixture<DataSourcesConfigComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DataSourcesConfigComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DataSourcesConfigComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
