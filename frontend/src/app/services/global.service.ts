import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class GlobalService {

  constructor() { }

  public baseUrl: string = '';
  public customerId: string = '';
  public developerToken: string = '';

  setBaseUrl(url: string) {
    this.baseUrl = url;
  }

  setCustomerId(id: string) {
    this.customerId = id;
  }

  setDeveloperToken(token: string) {
    this.developerToken = token;
  }
}