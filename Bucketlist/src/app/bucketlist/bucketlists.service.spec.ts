import { TestBed, inject } from '@angular/core/testing';

import { BucketlistsService } from './bucketlists.service';

describe('BucketlistsService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [BucketlistsService]
    });
  });

  it('should be created', inject([BucketlistsService], (service: BucketlistsService) => {
    expect(service).toBeTruthy();
  }));
});
