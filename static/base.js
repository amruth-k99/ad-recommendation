function AdvertisementList({ initialAdvts, onAdClick }) {
  return (
    <ul className="space-y-4">
      {initialAdvts.map((Advertisement) => (
        <li
          key={Advertisement["Ad Topic Line"]}
          className="bg-white p-4 rounded shadow cursor-pointer hover:bg-gray-50 transition"
          onClick={() => onAdClick(Advertisement)}
        >
          <h2 className="text-xl font-semibold">
            {Advertisement["Ad Topic Line"]}
          </h2>
          <p className="text-gray-600">
            City: {Advertisement.City}, Country {Advertisement.Country}
          </p>
          <p className="text-gray-600">
            Daily Internet Usage : {Advertisement["Daily Internet Usage"]} MB
            Daily Time Spent on Site :{" "}
            {Advertisement["Daily Time Spent on Site"]} minutes
          </p>
        </li>
      ))}
    </ul>
  );
}
