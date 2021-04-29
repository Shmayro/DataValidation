import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StandardisationComponent } from './standardisation.component';

describe('StandardisationComponent', () => {
  let component: StandardisationComponent;
  let fixture: ComponentFixture<StandardisationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ StandardisationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(StandardisationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
