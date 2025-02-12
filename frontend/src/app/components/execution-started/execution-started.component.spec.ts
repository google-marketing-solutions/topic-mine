import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExecutionStartedComponent } from './execution-started.component';

describe('ExecutionStartedComponent', () => {
  let component: ExecutionStartedComponent;
  let fixture: ComponentFixture<ExecutionStartedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ExecutionStartedComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ExecutionStartedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
