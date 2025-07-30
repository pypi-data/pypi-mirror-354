# CASE Mapping Python

## About the purpose and origins of this tool

<img src="img/proj-logo.png" align="left" height=80 alt="INSPECTr Logo" >
<img src="img/EU-H2020.jpg" align="right" alt="EU Flag" height=45>
</br></br></br></br>


This tool allows the user to create a .json formatted CASE Bundle and add entities from the CASE and UCO ontologies. Work on it begun in 2020 as part of  the [INSPECTr project](https://inspectr-project.eu/) which received funding from the European Union’s Horizon 2020 research and innovation programme, under grant agreement No 833276. It was created for the internal purposes of the project and originally named _CASE Builder_. It was developed by Ray Genoe, Cormac Doherty, and Robert Dowdall of [UCD - Centre for Cybersecurity and Cybercrime Investigation](https://www.ucd.ie/cci/) and Panos Protopapas of [Inlecom Innovation](https://inlecom.gr/). Throughout the development process Fabrizio Turchi of [CNR](https://www.cnr.it/en) aided the development by raising issues relating to (i) the creation of new CASE/UCO entities and (ii) changes that would make the tool more "CASE compliant".


## Usage

In a nutshell, in order to create a CASE file you need to:

- Create _Facets_ describing all the information you'd like to record (_Device Facets_ to describe devices, _Email Address
  Facets_ to describe email addresses, etc.).
- Append _Facets_ to _Objects_ that "enclose" them. The type of object depends on the facet; e.g, a
  _Device Facet_ should be enclosed by an _Observable Object_. More than one _Facet_ can be enclosed by the same object.
  For example, an _Investigative Action_ Object can enclose both a _Device Facet_ and an _Action Facet_ (describing an
  investigative action performed on the device).
- Append _Objects_ to a _CASE Bundle_.


## Codebase Structure

The central part of the codebase is located inside [base.py](case_mapping/base.py) that contains two classes (`FacetEntity`, `ObjectEntity`) and a helper function:

- `FacetEntity` is the class that all ontology classes are inheriting from either directly (in the case of facet-classes) or through `ObjectEntity` (in the case of object-classes). `FacetEntity` includes all the type checking (e.g., that `int` types are provided where integers are expected according to the ontology) as well as error handling when incorrect data-types are passed.
- `ObjectEntity` inherits `FacetEntity` and adds an `@id` value (random generated _uuid4_ string) to all classes inheriting from it. It also provides methods to append facet-classes to an object-class.
- All classes included within all modules in the _case_ and _uco_ folders inherit from either of these two classes, depending on whether these are facets or objects.

Moreover, all modules within the _case_ and _uco_ folders include a `directory` variable; a dictionary returning a class object when provided with the class's type (the classes `@type` value). The [directory.py](case_mapping/directory.py) module then aggregates all these variables and can be imported by the user and used when they require to create classes based on their type.

## Example Usage

> All instructions below follow the CASE bundle creation example provided in [example.py](../example.py) which can be run via `python3 example.py`. Note that at any point in the example printing an object will return the object's contents (as a pretty-printed dictionary).

Import the package. This will provide access to the `uco` and `case` libraries where all object classses are located. The naming of all UCO and CASE classes follows that found in the equivalent ontologies, e.g., the _Bundle_
class found in _uco-core_ of the UCO ontology, is provided at `uco.core.Bundle` in the builder.

```python
from case_mapping import *
```

Generate a _CASE Bundle_ by calling on the `Bundle` object from `uco.core`, adding an (optional) `uco_core_name`. Also create an empty array where the
investigative items will be appended at.

```python
bundle = uco.core.Bundle(uco_core_name="A Deepthought Case File")

investigation_items = []
```

To report an observable (a device in this example) create an _Observable Object_ (`cyber_item1`) and a _Device Facet_ (`device1`) and append the facet to the object. Finally, add
the observable (and appended facet) to the bundle.

```python
cyber_item1 = uco.observable.ObservableObject()
device1 = uco.observable.FacetDevice(manufacturer="Canon", model="PowerShot SX540")
cyber_item1.append_facets(device1)
bundle.append_to_uco_object(cyber_item1)
```

To report the existence, contents, and related metadata of a paricular file in the _Bundle_, create an observable and
append it to the array of `investigation_items`. Create a _File Facet_, a _Content Data Facet_, a _Raster Picture Facet_,
and an _EXIF Data Facet_, and append all to the observable. Finally, add the observable to the bundle.

```python
cyber_item2 = uco.observable.ObservableObject()
investigation_items.append(cyber_item2)  # NOTE: Appending whole object not just id
file1 = uco.observable.FacetFile(file_system_type="EXT4", file_name="IMG_0123.jpg", file_path="/sdcard/ImG_0123.jpg",
                                 file_extension="jpg", size_bytes=35002)
file_content1 = uco.observable.FacetContentData(byte_order="BigEndian", magic_number="/9j/ww==",
                                                mime_type="image/jpg", size_bytes=35000,
                                                data_payload="<base 64 encoded data of the file>",
                                                hash_method="SHA256",
                                                hash_value="6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b")
file_raster1 = uco.observable.FacetRasterPicture(picture_type="jpg", picture_height=12345, picture_width=12346, bits_per_pixel=2)
exif = {"Make": "Canon", "Model": "Powershot"}
file_exif1 = uco.observable.FacetEXIF(**exif)
cyber_item2.append_facets(file1, file_content1, file_raster1, file_exif1)
bundle.append_to_uco_object(cyber_item2)
```

To report an investigative action performed on a particular observable (a device in this example), create an
_Investigation Action_ and as before, append it to the `investigation items`. Append to the investigative action an _Action Reference Facet_ and a
_Device Facet_.

```python
inv_act = case.investigation.InvestigativeAction(name="annotated", end_time="2010-01-15T18:59:43.25Z", start_time="2010-01-15T17:59:43.25Z")
investigation_items.append(inv_act)  # NOTE: Appending whole object not just id
action_ref = uco.action.FacetActionReferences(performer="Dave", instrument="DiskAnalysisTool", environment="Lab", location="Dublin")
device2 = uco.observable.FacetDevice(device_type="iphone", manufacturer="apple", model="6XS", serial="77")
inv_act.append_facets(action_ref, device2)
bundle.append_to_uco_object(inv_act)
```

To report the relationship between two observables, create a _Cyber Relationship_ betweemn them and add it to the _Bundle_.

```python
cyber_rel1 = uco.observable.CyberRelationship(source=cyber_item1,  # created previously in the example
                                              target=cyber_item2,  # created previously in the example
                                              kind_of_relationship="Contained_Within")
path_rel1 = uco.observable.FacetPathRelation(path="/sdcard/IMG_0123.jpg")
cyber_rel1.append_facets(path_rel1)
bundle.append_to_uco_object(cyber_rel1)
```

For each e-mail account that must be reported, first create an observable appending to it an _Email Address Facet_. Then,
Then create a second observable appending to it an _Email Account Facet_, where when creating the latter you indicate the initial
"Email Address" observable as an `email_address`.

```python
email_address_object_1 = uco.observable.ObservableObject()
email_address_1 = uco.observable.FacetEmailAddress(email_address_value="test@test.com", display_name="George Test")
email_address_object_1.append_facets(email_address_1)

email_account_object_1 = uco.observable.ObservableObject()
account_1 = uco.observable.FacetEmailAccount(email_address=email_address_object_1)
email_account_object_1.append_facets(account_1)
bundle.append_to_uco_object(email_account_object_1)
```

To report an e-mail message, append an _Email Message Facet_ to an observable, and append the latter to the _Bundle_.

```python
cyber_item3 = uco.observable.ObservableObject()
email_msg = uco.observable.FacetEmailMessage(msg_to=[email_address_object_1, email_address_object_2],
                                             msg_from=email_address_object_1,
                                             subject="Revenge our father",
                                             body="To me, too, grant this boon-dark death to "
                                                  "deal unto Aegisthus, and to 'scape my doom.",
                                             received_time="2017-06-21T13:44:23.40Z",
                                             sent_time="2017-06-21T13:44:22.19Z",
                                             message_id="CAKBqNfyKo+ZXtkz6DUjWpvHy6"
                                                        "O82jTbkNA@mail.gmail.com")
cyber_item3.append_facets(email_msg)
bundle.append_to_uco_object(cyber_item3)
```

A phone number (or sms account) can be reported by appending a _Phone Account Facet_ to an observable.

```python
phone_account_object = uco.observable.ObservableObject()
phone_account1 = uco.observable.FacetPhoneAccount(phone_number="0035397876543")
phone_account_object.append_facets(phone_account1)
bundle.append_to_uco_object(phone_account_object)
```

An sms message can be reported by appending to an observable a _Message Facet_ where the sender and receiver(s) of the
sms message are reported by passing the observable objects holding the corresponding phone accounts as `msg_to` and `msg_from` properties;
similarly, the `application` property must be filled with an observable object holding an _Application Facet_.

```python
cyber_item4 = uco.observable.ObservableObject()
application_cyber_item = uco.observable.ObservableObject()
sms_application = uco.observable.FacetApplication(app_name="WhatsApp")
application_cyber_item.append_facets(sms_application)
sms_msg = uco.observable.FacetMessage(msg_to=[phone_account_object, phone_account_object2],
                                      msg_from=phone_account_object,
                                      message_text="A wedded wife, she slays her lord, "
                                                   "Helped by another hand!",
                                      sent_time="2017-06-20T09:34:42.12Z",
                                      application=application_cyber_item)
cyber_item4.append_facets(sms_msg)
bundle.append_to_uco_object(cyber_item4)
```

Reporting the identity of a person is done by first creating an _Identity Object_ and appending to it a _Simple Name Facet_, and (if known)
a _Birthday Information Facet_.

```python
identity = uco.identity.Identity()
identity_name = uco.identity.FacetSimpleName(given_name="Forename", family_name="Family-name")
identity_birth = uco.identity.FacetBirthInformation(birthdate="01-01-1988")
identity.append_facets(identity_birth, identity_name)
bundle.append_to_uco_object(identity)
```

To report a location, create a _Location Object_ and append to it a _Location Facet_.

```python
location1 = uco.location.Location()
lat_long = uco.location.FacetLocation(latitude=61.185055, longitude=9.468836)
location1.append_facets(lat_long)
bundle.append_to_uco_object(location1)
```

Finally, an _Investigation Object_ is being created where the `investigation actions` performed are being reported throught the
`core_objects` parameter.

```python
investigation = case.investigation.CaseInvestigation(focus="Transfer of Illicit Materials",
                                                     name="Crime A",
                                                     description="Inquiry into the transfer of illicit materials and "
                                                                 "the devices used to do so",
                                                     core_objects=investigation_items)
bundle.append_to_uco_object(investigation)
```
