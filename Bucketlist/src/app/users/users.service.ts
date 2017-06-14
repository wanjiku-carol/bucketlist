import { Injectable } from '@angular/core';
import { Http, Response, Headers } from '@angular/http';
import 'rxjs/add/operator/map';


@Injectable()
export class UsersService {

    constructor (
        private http: Http
    ) {}
    get(){
        return this.http.get('http://127.0.0.1:5000/auth/login/')
        .map((res:Response) => res.json());
    }
}
