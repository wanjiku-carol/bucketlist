import { Injectable } from '@angular/core';
import { Http, Response, Headers } from '@angular/http';
import 'rxjs/add/operator/map';

let bucketlists = [
    { title: 'Climb Mountains', isDone: true },
    { title: 'Buy Cars', isDone: true },
    { title: 'Wine Tasting', isDone: false },
    { title: 'Water Raft', isDone: false },
];
@Injectable()
export class BucketlistService {

    constructor (
        private http: Http
    ) {}
    get(){
        let headers = new Headers();
        headers.append('Authorization', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE0OTczNTcwMTAsInN1YiI6MSwiZXhwIjoxNDk3MzYwNjEwfQ.eCiJfKFxFJpRgRqlhH_Xaj9mnDoxzJHY6uBXeO1Ol_M');
        // return new Promise(resolve => resolve(bucketlists));
        return this.http.get('http://127.0.0.1:5000/bucketlists/', { headers })
        .map((res:Response) => res.json());
    }
}
