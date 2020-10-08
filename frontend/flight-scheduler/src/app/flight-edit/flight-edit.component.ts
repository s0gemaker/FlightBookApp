import {Component, OnInit} from '@angular/core';
import {BehaviorSubject, Observable} from 'rxjs';
import {Flight} from '../models/flight';
import {FlightService} from '../services/flight.service';
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-flight-edit',
  templateUrl: './flight-edit.component.html',
  styleUrls: ['./flight-edit.component.css']
})
export class FlightEditComponent implements OnInit {

  // flight: Observable<Flight>;
  _flight$ = new BehaviorSubject<Flight | null>(null);
  flight_id: number;
  success: boolean = false;
  trip_types = ['One Way', 'Round Trip', 'Multiple Destinations'];


  constructor(private flightService: FlightService,
              private activateRoute: ActivatedRoute) {
  }

  ngOnInit() {
    this.activateRoute.paramMap.subscribe(
      params => {
        this.flight_id = Number(params.get("id"));
      }
    );
    this.loadFlightData();
  }

  ngOnDestroy() {
    // best practice: complete all your subjects on component removal
    if (this._flight$ && !this._flight$.closed) {
      this._flight$.complete();
    }
  }

  loadFlightData() {
    this.flightService.getFlight(this.flight_id)
      .subscribe(data => this._flight$.next(data));
  }

  updateFlight() {
    this.flightService.updateFlight(this.flight_id, this._flight$)
      .subscribe(
        data => {
          // this._flight$ = data as Observable<Flight>;
          this.success = true;
        },
        error => console.log('Oops, can not update! ' + error)
      );
  }

  onSubmit() {
    this.updateFlight();
  }

}
