import { TestBed } from '@angular/core/testing';

import { GenerateAdsService } from './generate-ads.service';

describe('ConfigFormService', () => {
  let service: GenerateAdsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GenerateAdsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
