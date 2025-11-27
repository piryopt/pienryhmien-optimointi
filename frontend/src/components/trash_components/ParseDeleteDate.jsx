const ParseDeleteDate = ({ deletedAt }) => {
  const timestamp = Date.parse(deletedAt);
  const timeDate = new Date(timestamp);
  const nextWeek = new Date();
  nextWeek.setDate(timeDate.getDate() + 7);

  const day = nextWeek.getDate();
  const month = nextWeek.getMonth() + 1;
  const year = nextWeek.getFullYear();

  return `${day}.${month}.${year} 00:00`;
};

export default ParseDeleteDate;
