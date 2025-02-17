import { Component } from '@angular/core';

interface HistoryEntry {
  title: string;
  date: string;
  details: string;
  status: string;
}

@Component({
  selector: 'app-history',
  imports: [],
  templateUrl: './history.component.html',
  styleUrl: './history.component.css'
})
export class HistoryComponent {
  // TODO: RETRIEVE EXECUTION HISTORY FROM BACKEND
  // SHOULD THIS RETRIEVE TASKS FROM CURRENT INSTANCE, OR STORE EXECUTIONS IN A DATABASE?
  history: HistoryEntry[] = [
    {
      title: 'From Google Sheets',
      date: 'Feb 12, 2025',
      details: 'With keywords',
      status: 'Success'
    },
    {
      title: 'From BigQuery + Google Trends',
      date: 'Jan 24, 2025',
      details: 'With keywords, generic copies',
      status: 'Success'
    },
    {
      title: 'From Google Sheets + Google Trends',
      date: 'Jan 01, 2025',
      details: 'With keywords',
      status: 'Failed'
    },
    {
      title: 'From Google Sheets',
      date: 'Feb 12, 2025',
      details: 'With keywords',
      status: 'Success'
    },
    {
      title: 'From BigQuery + Google Trends',
      date: 'Jan 24, 2025',
      details: 'With keywords, generic copies',
      status: 'Success'
    },
    {
      title: 'From Google Sheets + Google Trends',
      date: 'Jan 01, 2025',
      details: 'With keywords',
      status: 'Failed'
    },
    {
      title: 'From Google Sheets',
      date: 'Feb 12, 2025',
      details: 'With keywords',
      status: 'Success'
    },
    {
      title: 'From BigQuery + Google Trends',
      date: 'Jan 24, 2025',
      details: 'With keywords, generic copies',
      status: 'Success'
    },
    {
      title: 'From Google Sheets + Google Trends',
      date: 'Jan 01, 2025',
      details: 'With keywords',
      status: 'Failed'
    },
    {
      title: 'From Google Sheets',
      date: 'Feb 12, 2025',
      details: 'With keywords',
      status: 'Success'
    },
    {
      title: 'From BigQuery + Google Trends',
      date: 'Jan 24, 2025',
      details: 'With keywords, generic copies',
      status: 'Success'
    },
    {
      title: 'From Google Sheets + Google Trends',
      date: 'Jan 01, 2025',
      details: 'With keywords',
      status: 'Failed'
    },
    {
      title: 'From Google Sheets',
      date: 'Feb 12, 2025',
      details: 'With keywords',
      status: 'Success'
    },
    {
      title: 'From BigQuery + Google Trends',
      date: 'Jan 24, 2025',
      details: 'With keywords, generic copies',
      status: 'Success'
    },
    {
      title: 'From Google Sheets + Google Trends',
      date: 'Jan 01, 2025',
      details: 'With keywords',
      status: 'Failed'
    },
    {
      title: 'From Google Sheets',
      date: 'Feb 12, 2025',
      details: 'With keywords',
      status: 'Success'
    },
    {
      title: 'From BigQuery + Google Trends',
      date: 'Jan 24, 2025',
      details: 'With keywords, generic copies',
      status: 'Success'
    },
    {
      title: 'From Google Sheets + Google Trends',
      date: 'Jan 01, 2025',
      details: 'With keywords',
      status: 'Failed'
    },
  ];
}
