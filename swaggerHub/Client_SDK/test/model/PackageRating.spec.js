/*
 * ECE 461 - Spring 2023 - Project 2
 * API for ECE 461/Spring 2023/Project 2: A Trustworthy Module Registry
 *
 * OpenAPI spec version: 2.0.0
 * Contact: davisjam@purdue.edu
 *
 * NOTE: This class is auto generated by the swagger code generator program.
 * https://github.com/swagger-api/swagger-codegen.git
 *
 * Swagger Codegen version: 3.0.41
 *
 * Do not edit the class manually.
 *
 */
(function(root, factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD.
    define(['expect.js', '../../src/index'], factory);
  } else if (typeof module === 'object' && module.exports) {
    // CommonJS-like environments that support module.exports, like Node.
    factory(require('expect.js'), require('../../src/index'));
  } else {
    // Browser globals (root is window)
    factory(root.expect, root.Ece461Spring2023Project2);
  }
}(this, function(expect, Ece461Spring2023Project2) {
  'use strict';

  var instance;

  describe('(package)', function() {
    describe('PackageRating', function() {
      beforeEach(function() {
        instance = new Ece461Spring2023Project2.PackageRating();
      });

      it('should create an instance of PackageRating', function() {
        // TODO: update the code to test PackageRating
        expect(instance).to.be.a(Ece461Spring2023Project2.PackageRating);
      });

      it('should have the property busFactor (base name: "BusFactor")', function() {
        // TODO: update the code to test the property busFactor
        expect(instance).to.have.property('busFactor');
        // expect(instance.busFactor).to.be(expectedValueLiteral);
      });

      it('should have the property correctness (base name: "Correctness")', function() {
        // TODO: update the code to test the property correctness
        expect(instance).to.have.property('correctness');
        // expect(instance.correctness).to.be(expectedValueLiteral);
      });

      it('should have the property rampUp (base name: "RampUp")', function() {
        // TODO: update the code to test the property rampUp
        expect(instance).to.have.property('rampUp');
        // expect(instance.rampUp).to.be(expectedValueLiteral);
      });

      it('should have the property responsiveMaintainer (base name: "ResponsiveMaintainer")', function() {
        // TODO: update the code to test the property responsiveMaintainer
        expect(instance).to.have.property('responsiveMaintainer');
        // expect(instance.responsiveMaintainer).to.be(expectedValueLiteral);
      });

      it('should have the property licenseScore (base name: "LicenseScore")', function() {
        // TODO: update the code to test the property licenseScore
        expect(instance).to.have.property('licenseScore');
        // expect(instance.licenseScore).to.be(expectedValueLiteral);
      });

      it('should have the property goodPinningPractice (base name: "GoodPinningPractice")', function() {
        // TODO: update the code to test the property goodPinningPractice
        expect(instance).to.have.property('goodPinningPractice');
        // expect(instance.goodPinningPractice).to.be(expectedValueLiteral);
      });

    });
  });

}));