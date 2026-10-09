import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class GenerateAdsService {
  constructor() {}

  // Observable sources
  private generateAdsSource = new Subject<any>();

  // Observable streams
  generateAds$ = this.generateAdsSource.asObservable();

  // Service message commands
  generateAds(configFormData: any) {
    this.generateAdsSource.next(configFormData);
  }
}
